let server_url = 'http://192.168.56.105:8008'

/***
 * http请求(流式响应处理)
 * @param url
 * @param data
 * @param func
 * @returns {Promise<void>}
 */
async function readChatbotReply(url,data={},func) {
    const response = await fetch(server_url+url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=UTF-8',
        },
        timeout:15000,
        body: JSON.stringify(data)
    });

  const readableStream = response.body;
  if (readableStream) {
    const reader = readableStream.getReader();
    let first = true
    while (true) {
      const { value, done } = await reader.read();
      if (done) {
        break;
      }

      const chunkValue = new TextDecoder().decode(value);
      // 流式返回的信息，在这里处理您的业务
      func(first,chunkValue)
      first = false
    }
    // Stream fully consumed
    reader.releaseLock();
  }
}