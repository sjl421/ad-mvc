var log = console.log.bind(console)

var e = function(sel) {
    return document.querySelector(sel)
}

var es = function(sel) {
    return document.querySelectorAll(sel)
}

// 转义 HTML，预防 XSS
var escapedHTML = function(html) {
    var d = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;',
    }

    var ks = Object.keys(d)
    // js string 需要使用正则才能实现 replace all
    var re = new RegExp(`[${ks.join('')}]`, 'g')
    html = html.replace(re, function(k) { return d[k] })

    return html
}

// ajax 函数
var ajax = function(method, path, data, responseCallback) {
    var r = new XMLHttpRequest()
    // 设置请求方法和请求地址
    r.open(method, path, true)
    // 设置发送的数据的格式为 application/json
    r.setRequestHeader('Content-Type', 'application/json')
    // 注册响应函数
    r.onreadystatechange = function() {
        // 4 表示 response 接收完毕
        if(r.readyState === 4) {
            // r.response 存的就是服务器发过来的放在 HTTP BODY 中的数据
            var response = JSON.parse(r.response)
            // ajax 无法直接完成跳转，此处约定“用一个 error 字段作为失败的标记”
            var error = response.error
            if (error) {
                alert(error)
            } else {
                responseCallback(response)
            }
        }
    }
    // 把数据转换为 json 格式字符串
    var data = JSON.stringify(data)
    // 发送请求
    r.send(data)
}
