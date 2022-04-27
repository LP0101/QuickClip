# QuickClip

**QuickClip is in very early development.**

QuickClip is a self hosted application that allows quick and easy video sharing.
Once you upload a video, it gets saved to `$QUICKCLIP_LIBRARY_PATH` with a random 8 character name. It can then be played back by accessing `/v/${video_name}`

## How to run it

### Config Variables

`QUICKCLIP_LIBRARY_PATH`: (Required) Path to store new video and look for existing ones.

`QUICKCLIP_ALLOWED_UPLOAD`: (Optional) CIDR range of allowed networks to upload.

### Running in Docker

`docker run -v ${host_video_path}:/clips -e QUICKSYNC_LIBRARY_PATH='/clips' -p 5000:5000 ghcr.io/lp0101/quickclip:latest` will serve the application on `localhost:5000`

## Future Plans

Future plans for the project:

* Encode uploaded videos to ensure they're all in the same format and playable through HTML5 video
* Add a way to browse/manage uploaded videos via the webUI directly
* Add real authentication options
* Add a parameter(s) for how many videos to keep. Age, number, etc