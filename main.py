from Interface import Interface

def main():
    interface = Interface()
    interface.run()

try:
    if __name__ == "__main__": main()

except Exception as e:
    print(e)
    input()
