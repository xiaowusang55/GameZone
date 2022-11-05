class GameDetailDM:

    def __init__(self, game_cn_name='', game_original_name='', game_total_story_time='',
                 game_release_date_and_platform='', game_type='', game_is_cn_supported='', game_producer='',
                 game_desc='',
                 game_player_tags='', game_pic_urls=''):
        self.row = (
            game_cn_name, game_original_name, game_total_story_time, game_release_date_and_platform, game_type,
            game_is_cn_supported, game_producer, game_desc, game_player_tags, game_pic_urls)
