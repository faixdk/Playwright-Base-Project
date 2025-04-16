import os
import re
import glob
import allure
from allure_commons.types import AttachmentType

def create_file_prefix(feature_name, scenario_name):
    """Create a safe file prefix from feature and scenario names"""
    safe_feature_name = re.sub(r'[^\w]', '_', feature_name).lower() if feature_name else "unknown_feature"
    safe_scenario_name = re.sub(r'[^\w]', '_', scenario_name).lower() if scenario_name else "unknown_scenario"
    return f"{safe_feature_name}_{safe_scenario_name}"

def take_screenshot(page, feature_name, scenario_name):
    """Take a screenshot and save it with a proper name"""
    # Create directories if they don't exist
    os.makedirs("reports/screenshots", exist_ok=True)
    os.makedirs("allure-results", exist_ok=True)

    file_prefix = create_file_prefix(feature_name, scenario_name)
    screenshot_path = f"reports/screenshots/{file_prefix}.png"

    try:
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        # Attach to Allure report
        try:
            allure.attach.file(
                screenshot_path,
                name="Screenshot on Failure",
                attachment_type=AttachmentType.PNG
            )

            # Also attach HTML content
            html_content = page.content()
            allure.attach(
                html_content,
                name="Page HTML on Failure",
                attachment_type=AttachmentType.HTML
            )
        except Exception as e:
            print(f"Failed to attach to Allure: {str(e)}")

        return screenshot_path
    except Exception as e:
        print(f"Failed to take screenshot: {str(e)}")
        return None

def process_videos(context, failed_scenarios):
    """Process videos from failed tests"""
    if not failed_scenarios:
        return

    print("Processing videos...")

    video_dir = 'reports/videos'
    os.makedirs(video_dir, exist_ok=True)

    # Create file prefix for the video
    file_prefix = create_file_prefix(
        failed_scenarios[0]['feature'],
        failed_scenarios[0]['scenario']
    )

    video_path = f"{video_dir}/{file_prefix}.webm"

    try:
        # Get the path of the original video file
        original_video_path = context.page.video.path()

        # Save as a new name directly (which will overwrite if exists)
        context.page.video.save_as(video_path)
        print(f"Video saved to {video_path}")

        # Delete the original video file to avoid duplication
        if os.path.exists(original_video_path) and original_video_path != video_path:
            os.remove(original_video_path)
            print(f"Removed original video: {original_video_path}")

        # Attach the video file to the report
        allure.attach.file(
            video_path,
            name="Test Execution Video",
            attachment_type=allure.attachment_type.WEBM
        )
        print("Video attached to Allure report")
    except Exception as e:
        print(f"Error processing video: {str(e)}")

def ensure_report_folders():
    """Ensure report folders exist"""
    os.makedirs("reports/screenshots", exist_ok=True)
    os.makedirs("reports/videos", exist_ok=True)
    os.makedirs("allure-results", exist_ok=True)