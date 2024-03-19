import glob, json
import subprocess
from pathlib import Path
import os
import ffmpy3
from .models import Course, Lesson


def get_duration_from_ffmpeg(url):
    tup_resp = ffmpy3.FFprobe(
        inputs={url: None},
        global_options=[
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format', '-show_streams'
        ]
    ).run(stdout=subprocess.PIPE)

    meta = json.loads(tup_resp[0].decode('utf-8'))
    return int(float(meta['format']['duration']))


def create_lesson_cover(media_path):
    # create the first frame of the video as the cover using ffmpy3
    cover_path = Path(media_path).with_suffix('.png')
    print(cover_path)
    if cover_path.exists():
        return str(cover_path)

    ffmpy3.FFmpeg(
        inputs={media_path: None},
        outputs={cover_path: ['-ss', '00:00:00.000', '-vframes', '1']}
    ).run()
    return str(cover_path)


def add_lesson(course):
    """
    This function is used to add lessons to a given course. It searches for media files in the course directory and
    creates a new lesson for each media file found. If a lesson with the same media file already exists in the database,
    it skips the creation of that lesson.

    Parameters:
    course (Course): The course object to which the lessons will be added.

    Returns:
    None
    """
    file_types = ('*.mp4', '*.avi', '*.mkv', '*.flv')
    media_files = []
    for ext in file_types:
        media_files.extend(glob.glob(course.course_path + '/**/' + ext, recursive=True))
    for i in range(len(media_files)):

        # check if the lesson is already in the database
        if Lesson.objects.filter(course=course, media=media_files[i]).exists():
            print('Lesson already exists in the database')
            continue
        lesson_title = Path(media_files[i]).name.strip(Path(media_files[i]).suffix)
        total_time = get_duration_from_ffmpeg(media_files[i])
        cover = create_lesson_cover(media_files[i])
        Lesson.objects.create(title=lesson_title, description=lesson_title, course=course, index_num=i + 1, cover=cover,
                              total_time=total_time, media=media_files[i])


def get_course_media():
    content = glob.glob('media/content/*', recursive=True)

    existing_courses_path = Course.objects.values_list('course_path', flat=True)
    if existing_courses_path:
        existing_courses_path = list(existing_courses_path)
    # compare the existing courses with the content, if the course is not in the database, add it
    for course_path in content:
        if course_path not in existing_courses_path:

            course_title = Path(course_path).name
            Course.objects.create(title=course_title, description=course_title, instructor=course_title,
                                  course_path=course_path)
            add_lesson(Course.objects.get(course_path=course_path))
