from playwright.sync_api import sync_playwright, expect
import time, sys, os, pickle, shutil, argparse
import pyautogui as ptg

parse = argparse.ArgumentParser("Youtube Playlist Downloader", description="Downloading youtube playlist")
parse.add_argument("-u", "--url", help="The url link of the playlist")
parse.add_argument("-r", "--restore", help="Restore the previous session", action="store_true")
args = parse.parse_args()



yt1 = True

cwd = os.getcwd()
target_path = os.path.join(cwd, "Music")
local_saved = os.path.join(cwd, "www")

restore = os.path.join(cwd, "data.dat")

if not args.restore and args.url == "" or args.restore and not os.path.exists(restore):
    parse.print_help()
    sys.exit(0)

filename_output = "Music"

if not os.path.exists(target_path):
    os.makedirs(target_path)
if not os.path.exists(local_saved):
    os.makedirs(local_saved)




def page_filter(route):
    if route.request.resource_type == "video":
        return route.abort()
    else:
        return route.continue_()


def get_yt_source_link(context):
    for page in context.pages:
        if "youtube.com" in page.url:
            return page.url


def print_message(message, error_type, from_function=""):
    error_list = {
        1: "[+] ",
        2: "[!] ",
        3: "[*!] ",
        4: "[*] Saved: "
    }
    if "" == from_function:
        error = f"{error_list[error_type]}{message}"
    else:
        error = f"{error_list[error_type]}{message}: {from_function}"
    print(error)

def pausing_video(page):
    try:
        expect(page.locator("button[title='Play (k)']")).to_be_visible(timeout=10000)
        button = page.locator("button[title='Play (k)']").last
        button.click()
    except:
        print_message("Unable to pause the video", 2, "pausing_video")


def new_page(context):
    page1 = context.new_page()
    return page1


def input_link_to_dl(page, timeout, yt_link):
    try:
        expect(page.get_by_placeholder("Search or paste Youtube link here")).to_be_visible(timeout=timeout)
        
        page.get_by_placeholder("Search or paste Youtube link here").fill(yt_link)
    except:
        print_message("Unable to find the input text", 3, "music_downloader_handler")
        sys.exit(0)

def music_downloader_handler(context, yt_link, converter_link):
    try:
        timeout = 500000
        page = context.new_page()
        page.goto(converter_link, timeout=timeout)
        input_link_to_dl(page, timeout, yt_link)
        if yt1:
            click_download(page, timeout)
            click_get_link(page, timeout)
        else:
            click_start(page, timeout)
            click_download4(page, 2000)
            click_download2(page, 2000)
        handling_download(page, timeout*100)
    except Exception as e:
        print(e)
        sys.exit(0)


def click_download4(page, timeout):
    print_message("Clicking Download button", 1)
    while True:
        if page.get_by_role("button", name="Download").is_visible(timeout=timeout):
            page.get_by_role("button", name="Download").click()
            break

def click_start(page, timeout):
    try:
        expect(page.get_by_role("button", name="Start")).to_be_visible(timeout=timeout)
        page.get_by_role("button", name="Start").click()
    except Exception as e:
        print_message(f"Unable to click start: {e}", 3, "Click Start")
        sys.exit(0)


def click_download(page, timeout):
    try:
        expect(page.get_by_text("Convert")).to_be_visible(timeout=timeout)
        page.get_by_text("Convert").first.click()
    except:
        print_message("Unable to locate submit", 2, "click_download")

def click_get_link(page, timeout):
    try:
        expect(page.get_by_text("Get link")).to_be_visible(timeout=timeout)
        page.get_by_text("Get link").click()
    except:
        print_message("Unable to locate get link", 3, "click_get_link")
        sys.exit(0)

# <div onclick="openMe(event)" class="convert_btn" id="convert_btn" data-authorization="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzExNTE0NDQsInJlZmVyZXIiOiJodHRwczovL2h0LmZsdnRvLm9ubGluZS8iLCJvcmlnaW4iOiJodHRwczovL2h0LmZsdnRvLm9ubGluZSIsInVzZXJBZ2VudCI6Ik1vemlsbGEvNS4wIChYMTE7IExpbnV4IHg4Nl82NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEzMC4wLjAuMCBTYWZhcmkvNTM3LjM2In0.-4mFqyBrWdj-9dXJv5DySYPG6Bb2LggP1NbtGm6TpAw" data-length="undefined" data-hash="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2aWRlb0lkIjoiNzMyaW16N0VhVDQiLCJleHQiOiJtcDMiLCJxdWFsaXR5IjozMjAsImV4cCI6MTczMTE1MDI0NH0.Kn-2pd8npqtQWMdRwiDu_9xj2AlrsiS0OoBqphFpOuQ"><div class="convert_btn_img"><img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzMiAzMiIgd2lkdGg9IjIwcHgiIGhlaWdodD0iMjBweCIgaWQ9ImRvd25sb2FkIj48ZyBkYXRhLW5hbWU9ImRvd25sb2FkIj48cGF0aCBkPSJNMjUsMTlhMSwxLDAsMCwwLTEsMXY1SDhWMjBhMSwxLDAsMCwwLTIsMHY1LjE0QTEuOTMsMS45MywwLDAsMCw4LDI3SDI0YTEuOTMsMS45MywwLDAsMCwyLTEuODZWMjBBMSwxLDAsMCwwLDI1LDE5WiI+PC9wYXRoPjxwYXRoIGQ9Ik0xNS4yNywyMC42OGwwLDBhMS4yLDEuMiwwLDAsMCwuMjYuMThsMCwwaDBBMSwxLDAsMCwwLDE2LDIxYTEsMSwwLDAsMCwuMzgtLjA4bC4xMi0uMDdhMS4xMywxLjEzLDAsMCwwLC4xOC0uMTJsMCwwLDAsMCw1LTUuMzhhMSwxLDAsMSwwLTEuNDYtMS4zN0wxNywxNy40NVY2YTEsMSwwLDAsMC0yLDBWMTcuNDVsLTMuMjctMy41MmExLDEsMCwxLDAtMS40NiwxLjM3WiI+PC9wYXRoPjwvZz48L3N2Zz4=" width="25px" height="25px"></div></div>

def click_download2(page, timeout):
    print_message("Clicking the convert btn", 1)
    # 1730 Y:  842 RGB: (167, 216, 220)

    page.bring_to_front()

    x = 1730
    y = 842
    time.sleep(5)
    ptg.click(x, y)



def click_download3(page, timeout):
    page.bring_to_front()
    time.sleep(20)
    x = 1730
    y = 842
    time.sleep(5)
    ptg.click(x, y)

def click_download1(page, timeout):
    try:
        expect(page.get_by_text("Download Now")).to_be_visible(timeout=timeout)
        page.get_by_text("Download Now").click()
    except:
        print_message("Unable to click download", 3, "click_download1")
        sys.exit(0)

def handling_download(page, timeout):
    print_message("Downloading", 1, "Handling Download")
    try:
        expect(page.get_by_text("Download Now")).to_be_visible(timeout=timeout)
        with page.expect_download() as pd:
            if yt1:
                click_download1(page, timeout)
            else:
                click_download3(page, timeout)
        download = pd.value
        path = os.getcwd()
        path = os.path.join(path, "Music", download.suggested_filename)
        print_message(f"Downloading: {download.suggested_filename}", 1, "")
        download.save_as(path)
        print_message(path, 4, "Handling Download")
    except:
        print_message("Unable to Find Download Now", 3, "Handling Download")
        sys.exit(0)
    # with page.expect_download() as pd:
    #     click_download1(page, timeout)
    # download = pd.value
    # path = os.getcwd()
    # path = os.path.join(path, "Music", download.suggested_filename)
    # download.save_as(path)
    # print_message(path, 4, "Handling Download")

def move_to_next_link(page, timeout):
    expect(page.locator("a[data-title-no-tooltip='Next']").first).to_be_visible(timeout=timeout)
    new_link = page.locator("a[data-title-no-tooltip='Next']").first.get_attribute("href")
    return new_link


def main(link, converter_link):
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:8080")
        context = browser.contexts[0]

        page = context.pages[0]

        page.route("**/*", page_filter)


        for page in context.pages:
            if len(context.pages) <= 1:
                break
            else:
                page.close()
        page.goto(link)
        first_time = True
        while True:

            if args.restore:
                link = move_to_next_link(page, 10000)


            print_message(f"Opening: {link}", 1)

            page.goto(link)

            music_downloader_handler(context, link, converter_link)
            
            with open(os.path.join(os.getcwd(), "data.dat"), "wb") as wfile:
                print_message(f"Saving link: {link}",1)
                pickle.dump(link, wfile)
            
            for page in context.pages:
                if "youtube.com" in page.url:
                    continue
                else:
                    page.close()
            
            page = context.pages[0]
            
            new_link = move_to_next_link(page, timeout=10000)
            link = new_link
            print()
            print()




if os.path.exists(os.path.join(os.getcwd(), "data.dat")) and args.restore:
    with open(os.path.join(os.getcwd(), "data.dat"), "rb") as rfile:
        print_message("Loaded", 1, "main")
        link = pickle.load(rfile)
else:
    link = args.url



if yt1:
    converter_link = "https://yt1s.com.co/en28/youtube-to-mp3/"
else:
    converter_link = "https://yt5s.is/en/youtube-to-mp3/"

try:
    main(link, converter_link)
except Exception as e:
    print(e)
    print_message("Please try to rerun the script again. The script probably failed to handle chrome", 3)
    sys.exit(0)


shutil.make_archive(filename_output, "zip", local_saved)