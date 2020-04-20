#!/bin/bash

# date = $1 (Ex:1115)
# URL = $2
# start time = $3 (Ex: 00:01:50)
# end time = $4

video1=("1115" "https://www.youtube.com/watch?v=N-QyKWMW4-0" "00:10:40" "00:34:09")
video2=("0930" "https://www.youtube.com/watch?v=RwSdcGSyl7Y" "00:02:41" "00:28:20")
video3=("0916" "https://www.youtube.com/watch?v=JuuiwgucGLg" "00:01:34" "00:13:19")
video4=("0805" "https://www.youtube.com/watch?v=fmGUinhmPrM" "00:05:00" "00:25:16")
video5=("0731" "https://www.youtube.com/watch?v=H973bI9FuhA" "00:03:24" "00:10:05")
video6=("0722" "https://www.youtube.com/watch?v=HqYfQC4vP2s" "00:02:01" "00:14:11")
video7=("0517" "https://www.youtube.com/watch?v=mbD5IKpKTsk" "00:02:50" "00:30:43")
video8=("0115" "https://www.youtube.com/watch?v=VkWjp379PbI" "00:02:42" "00:21:13")
video9=("1106" "https://www.youtube.com/watch?v=rpN9F0Ww1lM" "00:02:16" "00:26:49")
video10=("1231" "https://www.youtube.com/watch?v=ZYdFFWtm8Ac" "00:02:58" "00:25:21")
video11=("0108" "https://www.youtube.com/watch?v=d072tZup8Ko" "00:03:09" "00:29:25")
video12=("0113" "https://www.youtube.com/watch?v=dSkxRsNtPms" "00:02:29" "00:27:36")
video13=("0121" "https://www.youtube.com/watch?v=F5nGQP0bcNw" "00:01:29" "00:31:02")
video14=("0206" "https://www.youtube.com/watch?v=YD_0EmxiWoE" "00:03:35" "00:29:36")
video15=("0213" "https://www.youtube.com/watch?v=DhUU0W6VyFM" "00:03:35" "00:25:32")
video16=("0214" "https://www.youtube.com/watch?v=hs-Ze3Tk-Ts" "00:07:10" "00:39:14")
video17=("0220" "https://www.youtube.com/watch?v=5-9cWTTonC4" "00:02:46" "00:20:04")
video18=("0221" "https://www.youtube.com/watch?v=bEwba7I2uVA" "00:04:11" "00:40:24")
video19=("0225" "https://www.youtube.com/watch?v=soZDm0ikLPs" "00:00:51" "00:28:26")
video20=("0228" "https://www.youtube.com/watch?v=8I5YdmNtKEI" "00:03:11" "00:22:59")
video21=("0311" "https://www.youtube.com/watch?v=HRpDjcmNHqE" "00:01:32" "00:31:05")
video22=("0318" "https://www.youtube.com/watch?v=di3m8xJZnLM" "00:03:53" "00:30:08")
video23=("0320" "https://www.youtube.com/watch?v=f5x0pIA6f_M" "00:00:58" "00:24:45")
video24=("1204" "https://www.youtube.com/watch?v=G0EbkZptl6I" "00:02:08" "00:27:33")
video25=("1206" "https://www.youtube.com/watch?v=BG8zxSdKKpw" "00:04:33" "00:28:53")
video26=("1211" "https://www.youtube.com/watch?v=nYCYsQ_Ye_8" "00:02:26" "00:28:10")
video27=("1213" "https://www.youtube.com/watch?v=DhbV9yzrj1E" "00:02:30" "00:23:14")
video28=("0101" "https://www.youtube.com/watch?v=ATlEmj3u4Ls" "00:02:57" "00:21:39")
video29=("0114" "https://www.youtube.com/watch?v=8jh9a6nxT48" "00:04:10" "00:29:07")
video30=("0120" "https://www.youtube.com/watch?v=nfO9KsjDnIQ" "00:02:23" "00:30:32")
video31=("0122" "https://www.youtube.com/watch?v=3e9nGtGo4xY" "00:02:47" "00:28:08")
video32=("0203" "https://www.youtube.com/watch?v=Eyr1dcWCUTM" "00:00:46" "00:29:00")
video33=("0210" "https://www.youtube.com/watch?v=QMa9RYLPdas" "00:02:50" "00:40:29")
video34=("0523" "https://www.youtube.com/watch?v=ERFO-yoFBVA" "00:01:00" "00:28:19")
video35=("0524" "https://www.youtube.com/watch?v=zniwUcupsC4" "00:01:00" "00:23:24")
video36=("0531" "https://www.youtube.com/watch?v=B8eoGtADhYE" "00:02:25" "00:23:59")
video37=("0628" "https://www.youtube.com/watch?v=2CVB804oeL8" "00:01:43" "00:23:18")
video38=("0701" "https://www.youtube.com/watch?v=uX3hApSbXlY" "00:01:58" "00:28:35")
video39=("0719" "https://www.youtube.com/watch?v=AE4n1iQljNw" "00:04:02" "00:30:50")
video40=("0729" "https://www.youtube.com/watch?v=sDd1NuhOPxo" "00:03:57" "00:30:35")
video41=("0807" "https://www.youtube.com/watch?v=iIZKcxhklcc" "00:00:38" "00:16:21")
video42=("0812" "https://www.youtube.com/watch?v=ibq4XiK4UpQ" "00:04:04" "00:28:18")
video43=("0815" "https://www.youtube.com/watch?v=MwyyIOAek_k" "00:04:21" "00:26:54")
video44=("0816" "https://www.youtube.com/watch?v=iXsxmujTF6o" "00:02:07" "00:24:24")
video45=("0911" "https://www.youtube.com/watch?v=X5r8Hhtf3uw" "00:02:04" "00:31:01")
video46=("0918" "https://www.youtube.com/watch?v=gbzqj0IjRtA" "00:03:41" "00:25:38")
video47=("0925" "https://www.youtube.com/watch?v=cKpiGONo7NY" "00:00:32" "00:29:20")
video48=("0926" "https://www.youtube.com/watch?v=OfNS7oqX0Cc" "00:01:13" "00:29:59")
video49=("1007" "https://www.youtube.com/watch?v=OcVM7BlkpbI" "00:00:44" "00:26:58")
video50=("1008" "https://www.youtube.com/watch?v=5bqiK98bVGQ" "00:00:48" "00:25:26")
video51=("1014" "https://www.youtube.com/watch?v=MmljvssFEtE" "00:00:40" "00:25:26")
video52=("1029" "https://www.youtube.com/watch?v=OeuwFhrGB2k" "00:01:50" "00:31:39")
video53=("1118" "https://www.youtube.com/watch?v=gfeVCN65v0I" "00:01:21" "00:36:20")

all_videos=(
  video1[@]
  video2[@]
  video3[@]
  video4[@]
  video5[@]
  video6[@]
  video7[@]
  video8[@]
  video9[@]
  video10[@]
  video11[@]
  video12[@]
  video13[@]
  video14[@]
  video15[@]
  video16[@]
  video17[@]
  video18[@]
  video19[@]
  video20[@]
  video21[@]
  video22[@]
  video23[@]
  video24[@]
  video25[@]
  video26[@]
  video27[@]
  video28[@]
  video29[@]
  video30[@]
  video31[@]
  video32[@]
  video33[@]
  video34[@]
  video35[@]
  video36[@]
  video37[@]
  video38[@]
  video39[@]
  video40[@]
  video41[@]
  video42[@]
  video43[@]
  video44[@]
  video45[@]
  video46[@]
  video47[@]
  video48[@]
  video49[@]
  video50[@]
  video51[@]
  video52[@]
  video53[@]
)


COUNT=${#all_videos[@]}
for ((i=0; i<$COUNT; i++))
do
	DATE=${!all_videos[i]:0:1}
	URL=${!all_videos[i]:1:1}
	START_TIME=${!all_videos[i]:2:1}
	END_TIME=${!all_videos[i]:3:1}

	youtube-dl -f mp4 ${URL} -o videos/${DATE}.mp4 &&
	ffmpeg -i videos/${DATE}.mp4 -ss ${START_TIME} -to ${END_TIME} -c copy ./videos/${DATE}cut.mp4 &&
	rm videos/${DATE}.mp4 &&
	mkdir videos/${DATE}_images &&
	ffmpeg -i videos/${DATE}cut.mp4 videos/${DATE}_images/${DATE}%5d.png &&
	rm -r videos/${DATE}_images/*0.png &&
	rm -r videos/${DATE}_images/*2.png &&
	rm -r videos/${DATE}_images/*4.png &&
	rm -r videos/${DATE}_images/*6.png &&
	rm -r videos/${DATE}_images/*8.png &&
	./darknet detect cfg/yolov3.cfg yolov3.weights videos/${DATE}_images/ &&

	echo "DATE ${DATE}"
	# echo "URL ${URL}"
	# echo "START_TIME ${START_TIME}"
	# echo "END_TIME ${END_TIME}"
done

mv ../results ../results_old &&
mv ./results ../ &&
mv ../09face ../09face_old &&
cd ../../facenet &&
python identify.py


