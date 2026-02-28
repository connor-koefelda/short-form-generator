from gtts import gTTS
import subprocess

def generateTTS(script, output, lang='en', tld='com'):
    """Generates an audio based on a given script

    Args:
        script (str): The script for what should be said.
        output (str): Path to desired mp3 output location.  Recommended to end in .mp3.
        lang (str, optional): Language for TTS, only supports certain languages. Defaults to 'en'.
        tld (str, optional): Regional accent for given language based on domain, only supports certain domains. Defaults to 'com'.
    """
    print("Generating TTS...")
    prompt=script
    tts = gTTS(prompt, lang=lang, tld=tld) #returns mp4 audio using google transalte
    tts.save(output) #saves above audio to file
    print(f"TTS generated to {output}!")
    #ffmpeg -i test_audio.mp3 -filter_complex "[0:a]atempo=1.25[a]" -map "[a]" output.mp3
    print(f"Speeding up audio...")
    speedUpAudio(output, 1.50)
    print(f"Audio sped up!")

#used to speed up audio, amount=1.5 \equiv 1.5x speed
def speedUpAudio(audioPath, amount):
    try:
        command = [ #speed up audio
            "ffmpeg",
            "-y",
            "-i", audioPath,
            "-filter_complex", f"[0:a]atempo={amount}[a]", #amount=1.5 \equiv 1.5x speed
            "-map", "[a]",
            f"temp{audioPath}"
            ]

            
        subprocess.run(command, check=True)

        command = [ #replace the original with the (sped up) temp
            "powershell",
            "mv",
            "-Force",
            f"temp{audioPath}", audioPath
        ]

        subprocess.run(command, check=True)

    except subprocess.CalledProcessError as e:
        print(f" Something went wrong while cutting the video: {e}")
    except FileNotFoundError:
        print("FFmpeg isn't around D:")

if (__name__ == "__main__"):

    prompt = """Retail workers, servers, or anyone in customer service—what’s something you were never allowed to tell customers, even though you really wanted to?

    Top Responses:

    [User: SandwichWizard]
    At the sub shop I worked at, if a sandwich was dropped on the floor, we weren’t technically supposed to throw it out unless the customer saw. The manager’s exact words were, “Bread is like nature’s plate.” I started packing my own lunch.
    [User: KarenSlayer87]
    We used to “run out” of menu items not because we were out, but because the chef didn’t want to make them anymore. If you ordered chicken pot pie at 8 PM, you were basically signing up to be hated.
    [User: DuctTapeSolutions]
    I worked in a hardware store, and we were told to never tell customers that some of our “premium” products were just rebranded generic items from the same manufacturer. You’re paying $10 more for the exact same duct tape.
    [User: CoffeeFiend42]
    At the coffee shop I worked at, the “sugar-free” syrup wasn’t actually sugar-free for like two months because of a supplier issue. Management told us not to mention it unless someone specifically asked. RIP to the diabetics.
    [User: ShrimpQueen]
    We weren’t supposed to tell customers that the “fresh” seafood we advertised was frozen and shipped in from halfway across the country. The shrimp was basically older than some of the staff.
    [User: PhoneGuy34]
    When I worked at a phone store, we weren’t allowed to tell customers that the “free” case or screen protector we threw in was actually included in the price of the phone plan. People left thinking we were so generous.
    [User: Rent-a-Manager]
    At my old car rental job, we weren’t allowed to explain why insurance coverage was so expensive. Spoiler: It was pure profit. The policy barely covered anything, but you were expected to sell it like your life depended on it.
    [User: TacoWarrior1990]
    In fast food, we had a button for "extra meat," but if you ordered it during a rush, there was a 50% chance you’d just get charged extra without getting anything. We weren’t allowed to double-check after it left the kitchen.
    [User: NotARoomba]
    At a vacuum store I worked at, we weren’t allowed to tell people that half the “deals” during Black Friday were just the normal prices from a month ago. The boss would say, “It’s about the illusion of saving money.”
    [User: ChaoticNeutral101]
    When customers asked if we spit in the food, the official policy was to laugh it off and say, “Of course not!” Truthfully, though? I never saw it happen… but some of the cooks had serious anger issues. Stay nice to your servers."""
    tts = gTTS(prompt, "tts.mp3", lang='en', tld='co.uk')