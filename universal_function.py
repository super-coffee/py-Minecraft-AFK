def default_callback():
    pass


# oh，你要延迟，要不我们喝杯咖啡吧（大雾
# tips：请勿往里面传要阻塞的函数，否则你会误了正事儿的（大雾
def nonblocking_delay(delay_time, callback, args):
    start = time.time()
    while True:
        callback(*args)
        now = time.time()
        if now - start == delay_time:
            break

