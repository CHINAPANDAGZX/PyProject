import vlc
import time


def play(audio: str):
    """
    play audio from local file or online url, base on libvlc(python-vlc)
    :param audio: audio file path or online url
    :return: None
    """
    vlc_instance = vlc.Instance()                   # creating a basic vlc instance
    media_player = vlc_instance.media_player_new()  # creating an empty vlc media player
    media = vlc_instance.media_new(audio)           # media
    media_player.set_media(media)                   # put the media in the media player
    media.parse()                                   # parse the metadata of the file
    media_player.play()


if __name__ == '__main__':
    play('http://192.168.1.128:8080/audio.wav')
    # play('message.wav')
    for i in range(100):
        time.sleep(1)
