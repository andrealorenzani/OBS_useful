import requests
import urllib.parse

displayed = {}

def getTweet(url, encparams, referrer, name='Anonymous'):
    #payload = open("request.json")
    headers = {
        'content-type': 'application/json',
        'Referer': referrer,
        'x-twitter-auth-type': 'OAuth2Session',
        'x-client-uuid': '58cb0367-92c0-4cfe-8626-c6f0e855f387',
        'x-csrf-token': 'REDACTED',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0',
        'authorization': 'Bearer REDACTED',
        'Cookie': 'guest_id=REDACTED; dnt=1; ads_prefs="HBISAAA="; kdt=REDACTED; twid=u%3D16858208; auth_token=REDACTED; ct0=REDACTED; des_opt_in=Y; _twitter_sess=REDACTED; lang=it',
        'Accept-Charset': 'UTF-8',
        'X-Client-Transaction-Id': '1kZWmNKAn+GsxNCYLLk9WBvXKYuE9OFIr1QttZi24ctq0EK4Ik3vUKdPhNmVpilhn56aadZCRBAvs7KV753XGJw6Duw91w',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors', 
        'Sec-Fetch-Site': 'same-origin' 
        }
    #r = requests.post(url, data=payload, headers=headers)
    r = requests.get(url, params=urllib.parse.parse_qs(encparams),  headers=headers)
    from jsonpath_ng import jsonpath, parse
    import json
    jsonpath_expression = parse('$..search_timeline.timeline.instructions[*].entries[*]')
    result = []
    for match in jsonpath_expression.find(json.loads(r.text)):
        match = json.dumps(match.value)
        author = parse('$.content.itemContent..user_results.result.legacy.name').find(json.loads(match))
        id_str = parse('$.entryId').find(json.loads(match))
        quote = parse('$.content.itemContent.tweet_results.result.legacy.full_text').find(json.loads(match))
        if len(author)>0 and len(id_str)>0 and len(quote)>0 and not id_str[0].value.startswith('promoted'):
            if not displayed.get(id_str[0].value, None) or displayed.get(id_str[0].value, None) != quote[0].value:
                result.append({"id": id_str[0].value, "author": name if name else author[0].value, "quote": quote[0].value})
                displayed[id_str[0].value] = quote[0].value
    return result

def getTweetSNW():
    url = 'https://twitter.com/i/api/graphql/tOUz374Df84NaVVr3M1p6g/SearchTimeline'
    qs = 'variables=%7B%22rawQuery%22%3A%22%23shinenightwalk%22%2C%22count%22%3A20%2C%22querySource%22%3A%22typed_query%22%2C%22product%22%3A%22Top%22%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Afalse%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_media_download_video_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D'
    return getTweet(url, qs, 'https://twitter.com/search?q=%23shinenightwalk&src=typed_query')

def getTweetSNW2023():
    url = 'https://twitter.com/i/api/graphql/tOUz374Df84NaVVr3M1p6g/SearchTimeline'
    params = 'variables=%7B%22rawQuery%22%3A%22%23shinenightwalk2023%22%2C%22count%22%3A20%2C%22querySource%22%3A%22typed_query%22%2C%22product%22%3A%22Top%22%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Afalse%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_media_download_video_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D'
    return getTweet(url, params, 'https://twitter.com/search?q=%23shinenightwalk2023&src=typed_query&f=top')

def getTweetAndrea():
    url = 'https://twitter.com/i/api/graphql/tOUz374Df84NaVVr3M1p6g/SearchTimeline'
    params = 'variables=%7B%22rawQuery%22%3A%22%23shinenightwalk2023Andrea%22%2C%22count%22%3A20%2C%22querySource%22%3A%22typed_query%22%2C%22product%22%3A%22Top%22%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Afalse%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_media_download_video_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D'
    refer = 'https://twitter.com/search?q=%23shinenightwalk2023Andrea&src=typed_query&f=top'
    url2023 = 'https://twitter.com/i/api/graphql/tOUz374Df84NaVVr3M1p6g/SearchTimeline'
    params2023 = 'variables=%7B%22rawQuery%22%3A%22%23shinenightwalkAndrea%22%2C%22count%22%3A20%2C%22querySource%22%3A%22typed_query%22%2C%22product%22%3A%22Top%22%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Afalse%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_media_download_video_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D'
    refer2023 = 'https://twitter.com/search?q=%23shinenightwalkAndrea&src=typed_query&f=top'
    return getTweet(url2023, params2023, refer2023, None) + getTweet(url, params, refer, None)