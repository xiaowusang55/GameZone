class GameDetailDM:

    def __init__(self, game_cn_name='', game_original_name='', game_total_story_time='',
                 game_release_date_and_platform=None, game_type='', game_is_cn_supported='', game_producer='', game_desc='',
                 game_player_tags=None, game_pic_urls=None):
        if game_release_date_and_platform is None:
            game_release_date_and_platform = []
        if game_player_tags is None:
            game_player_tags = []
        if game_pic_urls is None:
            game_pic_urls = []

        self.row = (
            game_cn_name, game_original_name, game_total_story_time, game_release_date_and_platform, game_type,
            game_is_cn_supported, game_producer, game_desc, game_player_tags, game_pic_urls)
