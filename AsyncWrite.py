import threading, time
class AsyncWrite(threading.Thread):
    def __init__(self, text, out):
        threading.Thread.__init__(self)
        self.text = text
        self.out = out
    def run(self):
        f = open(self.out, "a")
        f.write(self.text+'\n')
        f.close
        time.sleep(2)
        print("Finished writing " + self.out)

def Main():
    message = input("Enter a string to store: ")
    background = AsyncWrite(message, 'out.txt')
    background.start()
    #background.join()

if __name__ == '__main__':
    Main()
