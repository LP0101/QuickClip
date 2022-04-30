# QuickClip

**QuickClip is in very early development.**

QuickClip is a self hosted application that allows quick and easy video sharing.
Once you upload a video, it gets saved to `$QUICKCLIP_LIBRARY_PATH` with a random 8 character name. It can then be played back by accessing `/v/${video_name}`

## How to run it

### Config Variables

| Variable                      | Description                                                                                                                                 | Default Value                 | Required |
|-------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|----------|
| QUICKCLIP_LIBRARY_PATH        | Path to store new video and look for existing ones.                                                                                         | None                          | Yes      |
| QUICKCLIP_ALLOWED_UPLOAD      | CIDR range of allowed networks to upload.                                                                                                   | 0.0.0.0/0                     | No       |
| QUICKCLIP_ENCODE_VIDEOS       | Whether to encode uploaded videos to a web-friendly format                                                                                  | false                         | No       |
| QUICKCLIP_ENCODE_PATH         | If using video encoding, where to store temporary unencoded files                                                                           | ${QUICKCLIP_LIBRARY_PATH}/enc | No       |
| QUICKCLIP_ENCODE_VIDEOS_NVENC | If encoding videos, use the nvenc encoder. Requires compatible nvidia GPU. If using Docker, requires nvidia runtime and `:nvidia` tag image | false                         | no       |

### Running in Docker

`docker run -v ${host_video_path}:/clips -e QUICKSYNC_LIBRARY_PATH='/clips' -p 5000:5000 ghcr.io/lp0101/quickclip:latest` will serve the application on `localhost:5000`

## Future Plans

Future plans for the project:

* Encode uploaded videos to ensure they're all in the same format and playable through HTML5 video
* Add a way to browse/manage uploaded videos via the webUI directly
* Add real authentication options
* Add a parameter(s) for how many videos to keep. Age, number, etc