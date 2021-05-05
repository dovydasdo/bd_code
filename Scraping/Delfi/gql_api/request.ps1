$articleId = $args[0]
$modeType = $args[1]
$orderBy = $args[2]
$limit = $args[3]
$offset = $args[4]
$limitReplies = $args[5]
$outFile = $args[6]

Invoke-WebRequest -Uri "https://api.delfi.lt/comment/v1/graphql" `
-Method "POST" `
-OutFile "$outFile"`
-Headers @{
"method"="POST"
  "authority"="api.delfi.lt"
  "scheme"="https"
  "path"="/comment/v1/graphql"
  "sec-ch-ua"="`"Google Chrome`";v=`"89`", `"Chromium`";v=`"89`", `";Not A Brand`";v=`"99`""
  "accept"="*/*"
  "dcid"="1889568962,1,1645187370,1613651370,2c08ba9b68eaf8b2ad92c75e004cc0aa"
  "sec-ch-ua-mobile"="?0"
  "user-agent"="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
  "origin"="https://www.delfi.lt"
  "sec-fetch-site"="same-site"
  "sec-fetch-mode"="cors"
  "sec-fetch-dest"="empty"
  "referer"="https://www.delfi.lt/"
  "accept-encoding"="gzip, deflate, br"
  "accept-language"="lt,en-US;q=0.9,en;q=0.8,ru;q=0.7,pl;q=0.6"
} `
-ContentType "application/json" `
-Body "{`"operationName`":`"cfe_getComments`",`"variables`":{`"articleId`":$articleId,`"modeType`":`"$modeType`",`"orderBy`":`"$orderBy`",`"limit`":$limit,`"offset`":$offset,`"limitReplies`":$limitReplies,`"orderByReplies`":`"DATE_DESC`"},`"query`":`"fragment CommentBody on Comment {\n  id\n  subject\n  content\n  created_time\n  created_time_unix\n  article_entity {\n    article_id\n    count_total\n    count_anonymous\n    __typename\n  }\n  vote {\n    up\n    down\n    sum\n    __typename\n  }\n  author {\n    id\n    customer_id\n    idp_id\n    __typename\n  }\n  parent_comment {\n    id\n    subject\n    __typename\n  }\n  quote_to_comment {\n    id\n    subject\n    __typename\n  }\n  reaction {\n    comment_id\n    name\n    reaction\n    count\n    __typename\n  }\n  count_replies\n  count_registered_replies\n  status\n  __typename\n}\n\nquery cfe_getComments(`$articleId: Int!, `$modeType: ModeType!, `$offset: Int, `$limit: Int, `$orderBy: OrderBy, `$limitReplies: Int, `$orderByReplies: OrderBy, `$lastCommentId: Int, `$commentsBefore: Boolean) {\n  getCommentsByArticleId(article_id: `$articleId) {\n    article_id\n    count_total\n    count_total_main_posts\n    count_registered\n    count_registered_main_posts\n    count_anonymous_main_posts\n    count_anonymous\n    comments(mode_type: `$modeType, offset: `$offset, limit: `$limit, orderBy: `$orderBy) {\n      ...CommentBody\n      replies(lastCommentId: `$lastCommentId, commentsBefore: `$commentsBefore, limit: `$limitReplies, orderBy: `$orderByReplies) {\n        ...CommentBody\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n`"}"
