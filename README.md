# QuickClip

How to run:

## Environment variables

`QUICKCLIP_LIBRARY_PATH`: (Required) Path to store new video and look for existing ones.
`QUICKCLIP_ALLOWED_UPLOAD`: (Optional) CIDR range of allowed networks to upload

## Docker

`docker run -v ${host_video_path}:/clips -e QUICKSYNC_LIBRARY_PATH='/clips' -p 5000:5000 ghcr.io/lp0101/quickclip:latest`