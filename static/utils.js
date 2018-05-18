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
    r.open(method, path, true)
    r.setRequestHeader('Content-Type', 'application/json')

    r.onreadystatechange = function() {
        // 4 表示 response 接收完毕
        if(r.readyState === 4) {
            var response = JSON.parse(r.response)
            // ajax 无法直接完成跳转，此处约定“用一个 error 字段作为失败的标记”
            if (response.error) {
                alert(response.error)
            } else {
                // 注册好的回调
                responseCallback(response)
            }
        }
    }

    var data = JSON.stringify(data)
    r.send(data)
}
