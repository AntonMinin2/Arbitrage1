#!/bin/bash

# Папки для входных и выходных файлов
input_dir="./savedvideo_DO"
output_dir="./savedvideo_PAST"

# Создать выходную папку, если её нет
mkdir -p "$output_dir"

# Цикл обработки каждого видео файла
for file in "$input_dir"/*.mp4; do
    echo "Processing file: $file"

    # Программа 1: Вращать видео и сохранить как промежуточный файл
    ffmpeg -i "$file" -vf "rotate=0.4285*PI/180" "${output_dir}/$(basename "${file%.mp4}_temp1.mp4")"

    # Программа 2: Установить битрейт
    ffmpeg -i "${output_dir}/$(basename "${file%.mp4}_temp1.mp4")" -b:v 14M -bufsize 14M -vf "format=yuv444p" "${output_dir}/$(basename "${file%.mp4}_temp2.mp4")"

    # Программа 3: Удалить метаданные и сохранить как промежуточный файл
    ffmpeg -i "${output_dir}/$(basename "${file%.mp4}_temp2.mp4")" -map_metadata -1 -c:v copy -c:a copy "${output_dir}/$(basename "${file%.mp4}_temp3.mp4")"

    # Программа 4: Увеличить громкость и сохранить как промежуточный файл
    ffmpeg -i "${output_dir}/$(basename "${file%.mp4}_temp3.mp4")" -af "volume=1.04" -c:v copy -c:a libmp3lame "${output_dir}/$(basename "${file%.mp4}_temp4.mp4")"

    # Программа 5: Добавить надпись и сохранить как промежуточный файл
    ffmpeg -i "${output_dir}/$(basename "${file%.mp4}_temp4.mp4")" -vf "drawtext=text='СМОТРИ ПРОФИЛЬ':fontcolor=white@0.25:fontsize=22:x=(w-text_w)/2:y=h-(text_h*4)" -c:a copy "${output_dir}/$(basename "${file%.mp4}_temp5.mp4")"

    # Программа 6: Плавное потухание в конце и сохранить как промежуточный файл
    duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "${output_dir}/$(basename "${file%.mp4}_temp5.mp4")")
    fade_out_start=$(echo "$duration - 1.2" | bc)
    ffmpeg -i "${output_dir}/$(basename "${file%.mp4}_temp5.mp4")" -filter_complex \
    "[0:v]fade=t=out:st=$fade_out_start:d=1.2,format=yuva420p[v]; \
     [0:a]afade=t=out:st=$fade_out_start:d=1.2[a]" \
    -map "[v]" -map "[a]" "${output_dir}/$(basename "${file%.mp4}_temp6.mp4")"

    # Программа 7: Изменение скорости видео до 1.04x и сохранить как промежуточный файл
    ffmpeg -i "${output_dir}/$(basename "${file%.mp4}_temp6.mp4")" -filter:v "setpts=0.9615*PTS" -filter:a "atempo=1.04" "${output_dir}/$(basename "${file%.mp4}_temp7.mp4")"

    # Программа 8: Увеличение контраста и сохранить как промежуточный файл
    ffmpeg -i "${output_dir}/$(basename "${file%.mp4}_temp7.mp4")" -vf "eq=contrast=0.97" -c:a copy "${output_dir}/$(basename "${file%.mp4}_temp8.mp4")"

    # Программа 9: Изменение тона и сохранить как промежуточный файл
    ffmpeg -i "${output_dir}/$(basename "${file%.mp4}_temp8.mp4")" -vf "eq=gamma_r=1.03:gamma_g=1.03:gamma_b=1.03" -c:a copy "${output_dir}/$(basename "${file%.mp4}_temp9.mp4")"

    # Программа 10: Добавление зернистости и сохранить как промежуточный файл
    ffmpeg -i "${output_dir}/$(basename "${file%.mp4}_temp9.mp4")" -vf "noise=alls=5:allf=t" -c:a copy "${output_dir}/$(basename "${file%.mp4}_temp10.mp4")"

    # Программа 11: Плавное появление и сохранить как промежуточный файл
    ffmpeg -i "${output_dir}/$(basename "${file%.mp4}_temp10.mp4")" -vf "fade=in:st=0:d=1.8" "${output_dir}/$(basename "${file%.mp4}_temp11.mp4")"

    # Программа 12: Улучшение качества и сохранить как промежуточный файл
    ffmpeg -i "${output_dir}/$(basename "${file%.mp4}_temp11.mp4")" -vf "scale=iw*2:ih*2,unsharp=5:5:1.0:5:5:0.0,eq=contrast=1.2:brightness=0.05:saturation=1.2,hqdn3d=1.5:1.5:6:6" -c:a copy "${output_dir}/$(basename "${file%.mp4}_processed.mp4")"

    # Программа 13: Изменить соотношение сторон на 9:16 и добавить черные полосы
    # ffmpeg -i "${output_dir}/$(basename "${file%.mp4}_processed.mp4")" -vf "scale=1080:-1:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" -c:a copy "${output_dir}/$(basename "${file%.mp4}_final.mp4")"

    # Удаление всех промежуточных файлов
    rm "${output_dir}/$(basename "${file%.mp4}_temp1.mp4")" "${output_dir}/$(basename "${file%.mp4}_temp2.mp4")" "${output_dir}/$(basename "${file%.mp4}_temp3.mp4")" \
       "${output_dir}/$(basename "${file%.mp4}_temp4.mp4")" "${output_dir}/$(basename "${file%.mp4}_temp5.mp4")" "${output_dir}/$(basename "${file%.mp4}_temp6.mp4")" \
       "${output_dir}/$(basename "${file%.mp4}_temp7.mp4")" "${output_dir}/$(basename "${file%.mp4}_temp8.mp4")" "${output_dir}/$(basename "${file%.mp4}_temp9.mp4")" \
       "${output_dir}/$(basename "${file%.mp4}_temp10.mp4")" "${output_dir}/$(basename "${file%.mp4}_temp11.mp4")"
done
