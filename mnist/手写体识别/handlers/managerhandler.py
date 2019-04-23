import tornado.websocket
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import json
from mnist_infer import infer
record = {
    "handlers":set(),}
class ManagerHandler(tornado.websocket.WebSocketHandler):
    def reg(self):
        # 刷新页面会关闭websocket
        # print(len(record["handlers"]))
        if self not in record["handlers"]:
            self.id = len(record["handlers"]) + 1
            # 把当前用户的连接加入handlers中
            record["handlers"].add(self)
    def open(self):
        # write_message并没有立即显示，而是在回调函数之后才显示
        # write_message发到前端由on_message处理, 由于js控制，
        # open函数执行完毕后执行on_message函数
        # py中传输字符串调用json.dumps方法
        return
    def on_close(self):
        # print("close")
        record["handlers"].remove(self)
    # sendMsg发送的消息被送到这里处理
    def on_message(self, message):
        # py中接受字符串调用json.loads方法
        msg = json.loads(message)
        if msg["type"] == "reg":
            # 并发会出错
            self.reg()
        elif msg["type"] == "data":
            image_arr = msg["imagedata"].split(",")
            # print(len(image_arr))
            rgba_img = np.array(image_arr).reshape(28,28,4).astype('uint8')
            rgba_img = rgba_img[:,:,3].reshape(1,28,28,1)
            # print((rgba_img[:,:,:3] == 0).all())
            # rgba_img = np.array(image_arr).astype('uint8')
            # rgb_img = Image.fromarray(rgba_img).convert('L')
            # print((np.array(list(rgb_img.getdata())) == 0).all() )
            # rgb_img = np.array(rgb_img).astype("float32")
            # rgb_img = rgb_img.reshape(1,28,28,1)
            # gravity= np.array([0.2989,0.5870,0.1140])
            # grayscale = np.dot(rgb_img,gravity).reshape(-1)
            # print((grayscale == 0).all())
            # result = grayscale.reshape(1, 28,28,1)
            infer(rgba_img)
            # print(infer(result))
            # with open("", "w") as f:
            #     f.write(str(grayscale))
            # print(grayscale.shape)
            # plt.imshow(grayscale, cmap='gray')
            # plt.show()
            # print(rgb_img.shape)