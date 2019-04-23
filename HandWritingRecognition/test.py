import tensorflow as tf
import os
#os.environ["CUDA_VISIBLE_DEVICES"] = "0"

a = tf.constant([1.0, 2.0, 3.0], shape=[3], name='a')
b = tf.constant([1.0, 2.0, 3.0], shape=[3], name='b')
c = a + b
# 通过log_device_placement参数来输出运行每一个运算的设备。
sess = tf.Session(config=tf.ConfigProto(log_device_placement=True)) #输出运行的设备
print(sess.run(c))

# 在配置好GPU的环境下,默认使用的设备就是GPU