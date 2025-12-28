import os
import logging
import base64
import argparse
from enum import Enum
from typing import Optional, List

from dotenv import load_dotenv
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field
from pdf2image import convert_from_path
import PIL.Image


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 1. API Client Setup
client = genai.Client(api_key=gemini_api_key)


# 2. Schema Definition (Pydantic)
class ClaimType(str, Enum):
    ACCIDENT = "accident"
    THEFT = "theft"
    MEDICAL = "medical"
    OTHER = "other"


class InsuranceClaim(BaseModel):
    policy_number: str = Field(
        ..., description="The policy number found in the document."
    )
    claimant_name: str = Field(
        ..., description="Full name of the person making the claim."
    )
    incident_date: Optional[str] = Field(
        None, description="Date of incident in YYYY-MM-DD format."
    )
    claim_amount: Optional[float] = Field(
        None, description="The total amount claimed. Return 0.0 if not found."
    )
    claim_type: ClaimType = Field(
        ..., description="Categorize the claim based on the description."
    )
    is_handwritten: bool = Field(
        ..., description="True if the majority of the form is handwritten."
    )
    confidence_score: int = Field(
        ..., description="Rate confidence of extraction from 1-10."
    )


# 3. Helper Functions
def encode_image(image_path):
    """Encodes a local image file to base64 for the API."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def convert_pdf_to_images(pdf_path) -> List[str]:
    """
    Converts ALL pages of a PDF to temporary JPEG files.
    Returns a list of file paths.
    """
    try:
        # This returns a list of PIL Image objects (one per page)
        images = convert_from_path(pdf_path)

        saved_files = []
        for i, img in enumerate(images):
            temp_path = f"temp_page_{i}.jpg"
            img.save(temp_path, "JPEG")
            saved_files.append(temp_path)

        return saved_files
    except Exception as e:
        logger.error(f"Failed to convert PDF: {e}")
        return []


# 4. Core Extraction Logic (Updated for Multi-Page)
def extract_data_from_document(file_path: str) -> Optional[InsuranceClaim]:
    logger.info(f"Processing file: {file_path}")

    temp_files = []  # Keep track to delete them later

    # Step A: Get a list of image paths (whether input was PDF or JPG)
    if file_path.lower().endswith(".pdf"):
        temp_files = convert_pdf_to_images(file_path)
        processing_paths = temp_files
    else:
        processing_paths = [file_path]  # Treat single image as a list of 1

    if not processing_paths:
        logger.error("No images to process.")
        return None

    try:
        # Step B: Prepare contents for Gemini
        # Gemini expects a list of parts, which can be text or images
        contents_payload = [
            "You are an expert insurance data entry specialist. "
            "Synthesize information from all pages to fill the fields."
        ]

        # Load images as PIL objects
        for img_path in processing_paths:
            try:
                img = PIL.Image.open(img_path)
                contents_payload.append(img)
            except Exception as e:
                logger.error(f"Failed to load image {img_path}: {e}")

        # Step C: Call Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents_payload,
            config={
                "response_mime_type": "application/json",
                "response_schema": InsuranceClaim,
            },
        )

        extracted_data = response.parsed
        logger.info("Extraction successful.")
        return extracted_data

    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        return None
    finally:
        # Cleanup: Delete all temporary page images
        for path in temp_files:
            if os.path.exists(path):
                os.remove(path)


if __name__ == "__main__":
    # 1. Setup the Argument Parser
    parser = argparse.ArgumentParser(
        description="Extract structured data from insurance documents."
    )

    # Add the --file argument (required)
    parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="Path to the PDF or Image file to process.",
    )

    parser.add_argument(
        "--output",
        type=str,
        required=False,
        help="Path to save the extracted JSON data.",
    )

    # Parse the arguments
    args = parser.parse_args()

    # 2. Check if file exists
    if os.path.exists(args.file):
        logger.info(f"Starting Extraction for: {args.file}")

        # 3. Run extraction using the provided filename
        result = extract_data_from_document(args.file)

        if result:
            json_output = result.model_dump_json(indent=2)
            logger.info("EXTRACTION SUCCESSFUL!")
            logger.info("-" * 30)
            logger.info(json_output)
            logger.info("-" * 30)

            if args.output:
                try:
                    with open(args.output, "w") as f:
                        f.write(json_output)
                    logger.info(f"Saved output to: {args.output}")
                except Exception as e:
                    logger.error(f"Failed to save output to file: {e}")
        else:
            logger.error("Extraction Failed. Check logs.")
    else:
        logger.error(f"Error: The file '{args.file}' was not found.")
