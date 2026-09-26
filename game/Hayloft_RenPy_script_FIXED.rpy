# ===================================================================
# HAYLOFT — THE COMPLETE NOIR EPIC (DIRECTOR'S CUT)
# ===================================================================

# -------------------------------------------------------------------
# ENGINE CONFIGURATION
# -------------------------------------------------------------------

init -2 python:
    if not hasattr(config, "screen_width") or config.screen_width is None:
        config.screen_width = 1920
        config.screen_height = 1080

    config.has_sound = True
    config.has_music = True
    config.has_voice = False
    config.default_text_cps = 35

# -------------------------------------------------------------------
# AUDIO DEFINITIONS 
# -------------------------------------------------------------------
define audio.bgm_gloomy = "audio/gloomy.mp3" #[cite: 7]
define audio.bgm_tension = "audio/mother-mother-ins.mp3" #[cite: 7]
define audio.bgm_ruins = "audio/廃墟に居る者.mp3" #[cite: 7]

# -------------------------------------------------------------------
# CINEMATIC TRANSITIONS & CAMERA FX
# -------------------------------------------------------------------

define flash = Fade(0.08, 0.0, 0.35, color="#ffffff")
define red_flash = Fade(0.15, 0.05, 0.60, color="#8a0c0c")
define gunshot_flash = Fade(0.04, 0.02, 0.55, color="#ffddaa")
define slow_dissolve = Dissolve(1.5)
define very_slow_dissolve = Dissolve(3.0)
define cinematic_fade = Fade(1.2, 0.8, 1.4, color="#07060a")
define quick_cut = Dissolve(0.08)
define camera_shake = vpunch
define heavy_shake = hpunch

transform bg_memory_haze:
    subpixel True
    matrixcolor SepiaMatrix(0.65) * BrightnessMatrix(-0.08)
    
transform bg_addiction_blur:
    subpixel True
    blur 4.0
    matrixcolor BrightnessMatrix(-0.1) * SaturationMatrix(0.4)

# -------------------------------------------------------------------
# STAGE TRANSFORMS (AUTO-DIM HIGHLIGHTING)
# -------------------------------------------------------------------

transform left_talk:
    subpixel True
    easein 0.2 xalign 0.22 yalign 1.0 xzoom -1.0 matrixcolor BrightnessMatrix(0.0) * SaturationMatrix(1.0)
transform left_silent:
    subpixel True
    easein 0.2 xalign 0.22 yalign 1.0 xzoom -1.0 matrixcolor BrightnessMatrix(-0.25) * SaturationMatrix(0.6)
transform right_talk:
    subpixel True
    easein 0.2 xalign 0.78 yalign 1.0 xzoom 1.0 matrixcolor BrightnessMatrix(0.0) * SaturationMatrix(1.0)
transform right_silent:
    subpixel True
    easein 0.2 xalign 0.78 yalign 1.0 xzoom 1.0 matrixcolor BrightnessMatrix(-0.25) * SaturationMatrix(0.6)

transform stage_left:
    subpixel True
    easein 0.25 xalign 0.12 yalign 1.0 xzoom -1.0 matrixcolor BrightnessMatrix(-0.25) * SaturationMatrix(0.6)
transform stage_left_active:
    subpixel True
    easein 0.25 xalign 0.12 yalign 1.0 xzoom -1.0 matrixcolor BrightnessMatrix(0.0) * SaturationMatrix(1.0)
transform stage_center:
    subpixel True
    easein 0.25 xalign 0.50 yalign 1.0 xzoom 1.0 matrixcolor BrightnessMatrix(-0.25) * SaturationMatrix(0.6)
transform stage_center_active:
    subpixel True
    easein 0.25 xalign 0.50 yalign 1.0 xzoom 1.0 matrixcolor BrightnessMatrix(0.0) * SaturationMatrix(1.0)
transform stage_right:
    subpixel True
    easein 0.25 xalign 0.88 yalign 1.0 xzoom 1.0 matrixcolor BrightnessMatrix(-0.25) * SaturationMatrix(0.6)
transform stage_right_active:
    subpixel True
    easein 0.25 xalign 0.88 yalign 1.0 xzoom 1.0 matrixcolor BrightnessMatrix(0.0) * SaturationMatrix(1.0)
transform center_solo:
    subpixel True
    xalign 0.50 yalign 1.0 xzoom 1.0 matrixcolor BrightnessMatrix(0.0)

# -------------------------------------------------------------------
# OBJECT / PROP TRANSFORMS 
# -------------------------------------------------------------------

transform prop_examine:
    subpixel True
    align (0.5, 0.4)
    zoom 0.0
    easein 0.4 zoom 1.2
    on hide:
        easeout 0.3 zoom 0.0 alpha 0.0

transform prop_floating:
    subpixel True
    align (0.5, 0.4)
    zoom 1.2
    yoffset 0
    easein 2.0 yoffset -15
    easeout 2.0 yoffset 0
    repeat

transform prop_ui_corner:
    subpixel True
    easein 0.5 align (0.95, 0.05) zoom 0.5

# -------------------------------------------------------------------
# CHARACTERS DEFINITIONS
# -------------------------------------------------------------------

define e = Character("Elena", color="#fca5a5", who_bold=True)
define n = Character("Noah", color="#93c5fd", who_bold=True)
define t = Character("Thomas", color="#ea580c", who_bold=True)
define m = Character("Mara", color="#86efac", who_bold=True)
define man = Character("Stranger", color="#cbd5e1", who_bold=True)
define narrator = Character(None, what_italic=True)

# -------------------------------------------------------------------
# STATE VARIABLES 
# -------------------------------------------------------------------

default elena_humanity = 5
default elena_ruthlessness = 0
default trust_noah = 0
default mara_bond = 0
default learned_orphan_secret = False
default addiction_level = 0
default investigation_progress = 0
default remembered_promise = False
default took_thomas_gun = False
default hid_in_tall_grass = False

# -------------------------------------------------------------------
# UNIVERSAL BULLETPROOF ASSET LOADER
# -------------------------------------------------------------------

init python:
    import os
    import re

    def clean_name(name):
        # Strips out all spaces, hyphens, dashes, and apostrophes
        return re.sub(r'[\s\-_—\']+', '', name.lower())

    # 1. Scan for absolutely every valid image in the game folder
    all_images = {}
    for dirpath, dirnames, filenames in os.walk(config.gamedir):
        if "gui" in dirpath or "cache" in dirpath: continue
        for f in filenames:
            ext = os.path.splitext(f)[1].lower()
            if ext in ['.png', '.jpg', '.jpeg', '.webp', '.jfif']:
                clean_stem = clean_name(os.path.splitext(f)[0])
                rel_path = os.path.relpath(os.path.join(dirpath, f), config.gamedir).replace("\\", "/")
                all_images[clean_stem] = rel_path

    # 2. Register Backgrounds (Immune to file extension/spacing changes) #[cite: 3]
    BACKGROUNDS = {
        "bg_barn_exterior_night": "barnexteriornight",
        "bg_barn_interior_night": "barninteriornight",
        "bg_bathroom_mirror": "bathroommirror",
        "bg_city_alley_night": "cityalleynight",
        "bg_city_street_daytime": "citystreetdaytime",
        "bg_city_street_rainy_night": "citystreetrainynight",
        "bg_country_road_night": "countryroadnight",
        "bg_farm_exterior_dawn": "farmexteriordawn",
        "bg_farm_exterior_night": "farmexteriornight",
        "bg_farm_field_night": "farmfieldnight",
        "bg_farmhouse_interior": "farmhouseinterior",
        "bg_hayloft_dawn": "hayloftdawn",
        "bg_hayloft_night": "hayloftnight",
        "bg_maras_apartment": "marasapartment",
        "bg_revenge_wall_apartment": "revengewallapartment",
    }
    
    sw, sh = getattr(config, "screen_width", 1920), getattr(config, "screen_height", 1080)
    
    for bg_var, search_key in BACKGROUNDS.items():
        if search_key in all_images:
            renpy.image(bg_var, Transform(all_images[search_key], xalign=0.5, yalign=0.5, xysize=(sw, sh), fit="cover", subpixel=True))
        else:
            renpy.image(bg_var, Transform(Solid("#0a080d"), xsize=sw, ysize=sh))

    # 3. Register Props (Prevents crashes if props are missing/misnamed) #[cite: 6]
    PROPS = {
        "prop_bag": "bakerybag",
        "prop_blanket": "blanket",
        "prop_briefcase": "briefcase",
        "prop_files": "manilafiles",
        "prop_bullet": "metalplate",
        "prop_bloody_tickets": "oldtickets",
        "prop_photos": "photos",
        "prop_pins": "pins",
        "prop_report": "report",
        "prop_tickets": "tickets",
        "prop_torch": "torch",
        "prop_yarn": "yarn",
        "prop_gun": "gun",
    }
    
    for prop_var, search_key in PROPS.items():
        if search_key in all_images:
            renpy.image(prop_var, all_images[search_key])
        else:
            # Silent invisible fallback so game NEVER crashes
            renpy.image(prop_var, Null()) 

    # 4. Register Characters (Filename-based parsing, immune to folder structures)
    for dirpath, dirnames, filenames in os.walk(config.gamedir):
        if "gui" in dirpath or "cache" in dirpath: continue
        for f in filenames:
            ext = os.path.splitext(f)[1].lower()
            if ext not in ['.png', '.jpg', '.jpeg', '.webp']: continue
            
            stem = os.path.splitext(f)[0]
            rel_path = os.path.relpath(os.path.join(dirpath, f), config.gamedir).replace("\\", "/")
            
            # Register direct filename 
            renpy.image(stem, rel_path)
            
            # Parse casting call expressions (e.g. elena_neutral_angry)
            parts = stem.lower().split('_')
            if len(parts) >= 2:
                char_name = parts[0]
                if parts[1] == "neutral":
                    expr = "_".join(parts[2:])
                    if expr:
                        renpy.image(f"{char_name} {expr}", rel_path)
                    else:
                        renpy.image(f"{char_name} neutral", rel_path)
                else:
                    expr = "_".join(parts[1:])
                    renpy.image(f"{char_name} {expr}", rel_path)


# ===================================================================
# PROLOGUE: THE TALL GRASS
# ===================================================================

label start:
    play music bgm_gloomy fadein 2.0 
    
    scene bg_farm_exterior_night
    with cinematic_fade

    narrator "There are places that do not forgive."
    narrator "Not because cold stone or rot-gnawed timber possess a soul."
    narrator "Not because the damp earth keeps portraits buried in its black silt."
    narrator "Places refuse to forgive because human beings do not leave without carving pieces of their sanity into the grain."
    
    narrator "Some places drink the blood of the people who work them, and in return, they give you corn, wheat, and silence."
    narrator "Vance Hollow was one of those places."

    narrator "A shared whisper smothered in the straw."
    narrator "The heat of two young lovers with their legs tied up in knots, defying the chill of October." #[cite: 4]
    narrator "A shotgun shell hitting a concrete floor."
    narrator "And a scream that traveled seven miles across the tall grass, completely unanswered by God or man."

    pause 1.5
    jump act1_the_house


# ===================================================================
# ACT I: THE FARM, THE BOY, AND THE BLOOD
# ===================================================================

label act1_the_house:
    scene bg_farmhouse_interior
    with very_slow_dissolve

    narrator "10:14 PM. October 24th."
    narrator "Inside the Vance farmhouse, every floorboard is a landmine waiting to detonate."
    narrator "The house smells of boiled cabbage, ancient dust, and the sharp, sour tang of cheap corn liquor."
    narrator "Elena Vance stands barefoot in the dark kitchen. She holds her leather boots tightly against her chest, her knuckles white."
    
    show elena tired at center_solo with dissolve
    
    narrator "From the master bedroom directly above her, the rhythmic, heavy snore of her father shakes the lathe and plaster."
    narrator "Thomas Vance has been drinking since the grain buyers from the city left at noon."
    narrator "When he is sober, he is an unforgiving warden with fists like cured hickory, a man who views his daughter not as family, but as property."
    narrator "He is a man of the old world. A man who believes the land owns you, and he owns the land."
    narrator "But when he drinks... he hears trespassers in the wind, thieves in the shadows, and conspiracy in every glance."
    
    narrator "The girl knew her family wouldn't like a city boy. Especially not Thomas. Knowing how abusive he was, an outsider sniffing around his daughter was a death sentence." #[cite: 4]

    e "{size=-2}Sleep, old man. Just stay asleep. Let the liquor drown you for just one night.{/size}"

    menu:
        "Check his rifle rack before slipping out into the night.":
            $ elena_ruthlessness += 1
            $ took_thomas_gun = True
            narrator "Elena creeps toward the gun cabinet beside the back door. The floorboards protest silently under her weight."
            narrator "The glass door is unlocked. The smell of gun oil, Hoppe's No. 9, and stale tobacco bites her nostrils."
            
            show prop_gun at prop_examine 
            narrator "The 12-gauge Remington pump sits loaded in its velvet cradle. Four red shells in the tube."
            e "{size=-2}My daddy's got a gun. If he wakes up and finds me missing, this is what he reaches for. I can't leave it loaded.{/size}"
            narrator "Her hand hovers over the cold blued steel."
            narrator "With agonizing slowness, she presses the shell release inside the loading port."
            narrator "{i}Snick.{/i}"
            narrator "She catches the first heavy red shell in her palm, slipping it into her coat pocket."
            narrator "She removes two more, leaving the chamber empty but the tube with just one shell."
            e "{size=-2}That should give me enough time to run if he comes looking.{/size}"
            hide prop_gun with dissolve
            narrator "She closes the cabinet door, the brass hinges screaming silently in the quiet house."

        "Slip out quietly without risking the creaky cabinet.":
            $ elena_humanity += 1
            $ took_thomas_gun = False
            e "{size=-2}Don't push your luck. Just get outside. The less time I spend in this house, the better.{/size}"
            narrator "She turns her back on the gun cabinet, refusing to engage with the instruments of his violence."
            narrator "She lifts the iron latch of the back door with millimetric precision, terrified that the scrape of metal will echo up the stairwell."

    narrator "The door opens. The crisp autumn air hits her face like a cold splash of river water."
    narrator "She slips through the gap and closes it behind her."

    scene bg_farm_field_night
    with slow_dissolve

    narrator "She sits on the rotting porch steps just long enough to lace her leather work boots, pulling the laces tight until they bite into her ankles."
    narrator "Then, she plunges into the tall grass and the rows of corn."
    
    narrator "The dry stalks whip against her coat like papery ghosts. To the south, eighty acres of dark crop stretch out under a sickle moon."
    narrator "She navigates by memory, counting the rows, avoiding the muddy washouts where the tractor tires dug deep ruts during the spring rains."
    
    narrator "Suddenly, a shadow shifts near the old poplar tree. The wind dies down, and a distinct rustle sounds to her left."
    
    menu:
        "Drop to the dirt and hide in the tall grass.":
            $ hid_in_tall_grass = True
            $ elena_ruthlessness += 1
            narrator "Elena instantly drops to her stomach, burying her face in the freezing mud and decaying husks."
            narrator "She holds her breath, her heart hammering against her ribs like a trapped bird."
            narrator "Footsteps crush the dry leaves nearby. A stray dog, or a coyote, trots past the poplar tree and disappears."
            narrator "She waits until her lungs burn before slowly standing back up."
            e "{size=-2}Paranoid. I'm getting as paranoid as he is.{/size}"

        "Freeze and stare into the darkness.":
            $ elena_humanity += 1
            narrator "Elena freezes, her eyes wide, staring into the impenetrable blackness between the stalks."
            narrator "A stray dog emerges from the gloom, its ribs showing against its mangy coat. It sniffs the air, looks at her, and trots away."
            narrator "She lets out a shaky breath, realizing her fists are clenched so tight her fingernails are cutting into her palms."

    narrator "Finally, she breaks through the last row of stalks."
    narrator "At the perimeter of the hollow sits the red silhouette of the great barn."

    scene bg_barn_exterior_night
    with dissolve

    narrator "The barn stands like an abandoned cathedral against the night sky, its red paint peeling like sunburned skin."
    narrator "It is a monument to a time when the Vance farm was prosperous, before the debts, before the drinking, before the absolute silence."
    narrator "A shadow separates itself from the rusted tractor frame near the silo."

    show noah neutral at right_talk with moveinright
    show elena nervous at left_silent with dissolve

    n "You're twenty minutes late, Vance. I was starting to think the old man chained you to the radiator."

    show elena tired at left_talk
    show noah neutral at right_silent
    e "It's not funny, Noah. My father sat at the kitchen table until ten staring at his ledger, drinking moonshine straight from the jar. I couldn't move until he passed out."

    show elena tired at left_silent
    show noah happy at right_talk
    n "I was about ready to pick the lock on your pantry window and carry you out over my shoulder."

    show elena angry at left_talk
    show noah happy at right_silent
    e "And end up with buckshot in your gut? He'd shoot you before you even set foot on the linoleum."
    e "He hates anyone from the city. He thinks you're all parasites. If he knew a city boy was sneaking onto the farm to see me, he'd kill you. Without a second thought."

    show elena angry at left_silent
    show noah thinking at right_talk
    n "Then it's a good thing I brought peace offerings instead of lockpicks. And I'm fast on my feet."

    show prop_bag at prop_examine 
    narrator "Noah pulls a warm paper parcel from inside his denim coat."
    narrator "The unmistakable aroma of sugar, butter, and baked cinnamon fills the cold air, cutting sharply through the smell of damp earth and rotting husks."
    hide prop_bag with dissolve

    menu:
        "Tease him about his late-night acquisitions.":
            $ trust_noah += 2
            show elena happy at left_talk
            show noah neutral at right_silent
            e "Henderson's bakery locked up five hours ago, Noah. Did you break another window latch?"
            show elena happy at left_silent
            show noah happy at right_talk
            n "I'll have you know I left three crumpled dollars on his flour bin. That makes it unconventional commerce, not burglary."

        "Kiss him right there in the frost.":
            $ trust_noah += 3
            $ elena_humanity += 2
            narrator "Elena steps forward, grabbing the lapels of his jacket and pulling his mouth down to hers."
            narrator "His skin is cold from waiting in the frost, but his breath is warm, tasting of brown sugar and crisp autumn air."
            show noah happy at right_talk
            n "Damn... if that's the welcome I get, I'll steal pastries from Henderson every single night."

        "Warn him to keep his voice down.":
            $ elena_ruthlessness += 1
            show elena nervous at left_talk
            show noah neutral at right_silent
            e "Shh! Keep your voice down. The valley carries sound like an amphitheater tonight."
            show elena nervous at left_silent
            show noah neutral at right_talk
            n "All right, all right. Point taken. Let's get up into the loft out of the wind. You're shivering."

    scene bg_barn_interior_night
    with dissolve

    narrator "They push open the heavy lower personnel door, wincing at the faint groan of the hinges."
    narrator "The ground floor is dark and vast, smelling of dry timothy, old manure, and damp stone."
    narrator "They used to sneak up to the barn, and towards the hayloft at night to talk for hours." #[cite: 4]
    narrator "The wooden ladder creaks precariously under their weight as they climb into the upper cathedral of the hayloft."

    scene bg_hayloft_night
    with slow_dissolve

    narrator "Moonlight slants through the open hay door, illuminating mountains of golden straw."
    narrator "Up here, insulated from the world below, it feels as if Thomas Vance and his violence belong to another planet."

    show elena neutral at left_silent
    show noah neutral at right_talk
    with dissolve

    n "Here. Sit. I kept the blanket hidden under the third bale."

    show prop_blanket at prop_examine 
    narrator "Noah spreads a heavy woolen work blanket over the straw. They sit shoulder to shoulder."
    hide prop_blanket with dissolve
    
    narrator "Elena eats the pastry slowly, feeling the knot in her stomach unravel for the first time in eighteen hours."

    show elena thinking at left_talk
    show noah neutral at right_silent
    e "My father said something today. While he was cleaning his boots on the porch."

    show elena thinking at left_silent
    show noah thinking at right_talk
    n "What did he say?"

    show elena thinking at left_talk
    show noah thinking at right_silent
    e "He said the tall boy from the city who works at the lumber yard has been seen lingering around our south acreage."
    e "He said... if he catches a city kid sniffing around his property, he'll treat him like a rabid coyote."
    
    show elena nervous at left_talk
    narrator "Elena turns to him, her fingers digging into the wool blanket."
    e "Noah, you need to stop walking down the county line road in daylight. He's not bluffing. He's never bluffing. You know how abusive he is." #[cite: 4]

    show elena nervous at left_silent
    show noah neutral at right_talk
    n "Elena, listen to me."
    narrator "Noah shifts, turning his body completely toward hers, his expression turning serious."
    n "I'm not spending another winter in this valley. I'm not watching you freeze in that house while he drinks himself into a rage."
    n "I've got three hundred dollars saved from the mill. In two weeks, the logging season ends."
    n "I went to the station yesterday."
    
    show prop_tickets at prop_examine 
    n "I bought two coach bus tickets to Chicago."
    
    show elena surprised at left_talk
    show noah neutral at right_silent
    e "Noah... you can't just..."

    show elena surprised at left_silent
    show noah happy at right_talk
    n "Yes, I can. And you're coming with me."
    n "We'll get a room in a building where nobody knows your father's name. A place with a radiator that actually works."
    hide prop_tickets with dissolve

    menu:
        "Commit fully to running away with him.":
            $ trust_noah += 3
            $ elena_humanity += 2
            show elena happy at left_talk
            show noah neutral at right_silent
            e "Chicago... God, Noah. You really bought the tickets?"
            show elena happy at left_silent
            show noah happy at right_talk
            n "Tucked right inside my wallet. October twenty-ninth. Midnight departure."
            e "I'll do it. I swear to you, I'll pack one satchel and meet you at the depot."

        "Express your terrifying doubt that Thomas will let you go.":
            $ elena_ruthlessness += 1
            show elena thinking at left_talk
            show noah neutral at right_silent
            e "You don't understand him, Noah. He doesn't just let things leave."
            e "When the farmhands tried to quit last year, he tracked them down to the county line and beat them with a tire iron. He hunts what belongs to him."
            show elena thinking at left_silent
            show noah thinking at right_talk
            n "He's an old man with bad knees and an empty whiskey bottle, Elena. He can't chase a bus across three states."

    narrator "Noah reaches out, his fingers sliding along her jaw, pulling her gaze back to him."
    narrator "In the quiet of the hayloft, the cold outside dissolves into something urgent and fragile."
    narrator "They lie back into the sweet straw, holding each other as if the morning might never dare to come."
    
    scene bg_hayloft_night
    with cinematic_fade
    
    narrator "For hours, they talk, and they make love, young lovers with their legs tied up in knots." #[cite: 4]
    narrator "For a brief, fleeting moment in time, the Vance farm does not exist. There is only the loft, the moonlight, and the absolute certainty that they will escape."
    narrator "It was all perfect." #[cite: 4]

    $ remembered_promise = True

    show elena happy at left_talk
    show noah happy at right_silent
    with dissolve
    
    e "Noah?"

    show elena happy at left_silent
    show noah neutral at right_talk
    n "Yeah?"

    show elena nervous at left_talk
    show noah neutral at right_silent
    e "Promise me. When we get on that bus... don't ever let me come back."
    e "No matter what happens. No matter if I get scared, or if I say I left something behind. Promise me this dirt will never see my face again."

    show elena nervous at left_silent
    show noah neutral at right_talk
    n "I promise, Elena. On my life. I'll tie you to the seat if I have to."

    pause 1.5

    # ===============================================================
    # THE INTRUSION
    # ===============================================================

    scene bg_hayloft_night
    with dissolve

    narrator "1:22 AM."
    
    stop music fadeout 2.0
    
    narrator "A sudden, freezing draft sweeps up through the loft floor, disturbing the dust motes."
    narrator "The ambient hum of the crickets outside abruptly stops."

    show elena scared at left_talk
    show noah nervous at right_silent
    with dissolve

    e "{cps=15}...The wind changed.{/cps}"

    show elena scared at left_silent
    show noah thinking at right_talk
    n "Elena?"

    show elena scared at left_talk
    show noah thinking at right_silent
    e "{cps=15}The lower barn door. Did you bar it?{/cps}"

    show elena scared at left_silent
    show noah nervous at right_talk
    n "I pulled it shut... I didn't see a drop bar on the outside jamb. I thought it was stuck."

    narrator "From down below, in the pitch-black maw of the tractor bay:"
    narrator "{i}SCREEECH.{/i}"
    narrator "The massive wooden barn door was open and creaking, its rusted iron hinges screaming in the quiet night." #[cite: 4]

    with camera_shake
    narrator "{size=+4}THUD.{/size}"
    narrator "A loud thud sound appeared from the front of the barn." #[cite: 4]
    
    show elena scared at left_talk
    show noah scared at right_silent
    e "{size=-2}Oh God. He's here. Noah, he's down there. He woke up.{/size}"

    show elena scared at left_silent
    show noah scared at right_talk
    n "{size=-2}The rear loft hatch. We can drop onto the hay trailer outside, run for the treeline—{/size}"

    narrator "It was a gunshot. A warning shot fired directly into the ceiling joists of the first floor." #[cite: 4]

    play music bgm_tension fadein 1.0 

    t "{size=+6}ELENA!{/size}"

    narrator "The roar rattles the very roof of the barn, shaking loose decades of dust."
    narrator "They both got startled." #[cite: 4]
    narrator "Heavy, violent footsteps pound up the wooden stairs. Not the steps of an old, drunk man, but the driven, furious stomp of a predator."

    scene bg_hayloft_night
    with flash

    # 3 Characters fully staged
    show elena scared at stage_left
    show noah scared at stage_center
    show thomas angry at stage_right
    with heavy_shake

    narrator "The door flew open and her father stood there with a gun." #[cite: 4]
    narrator "My daddy's got a gun, you better run."
    
    if took_thomas_gun:
        narrator "He is holding his backup piece, a rusted double-barrel coach gun. He must have realized the Remington was emptied."
    else:
        narrator "He is holding the 12-gauge Remington pump, its blued barrel gleaming maliciously in the moonlight."

    show thomas angry at stage_right_active
    show noah scared at stage_center
    show elena scared at stage_left
    t "YOU SLUT! YOU FILTHY, WHORING LITTLE TRAITOR!"
    
    narrator "He looked at both of them, all vulnerable in the hay, and started screaming." #[cite: 4]

    show thomas angry at stage_right
    show elena scared at stage_left_active
    e "Dad, don't! Please! Put the gun down! We haven't done anything!"

    narrator "The daughter tried to explain but he heard nothing. His eyes were wide, unblinking, swallowed by alcohol and absolute rage." #[cite: 4]

    show elena scared at stage_left
    show thomas angry at stage_right_active
    t "Shut your lying mouth! I saw him creeping across my corn! City parasite sneaking into my barn to violate my flesh and blood!"

    show thomas angry at stage_right
    show noah scared at stage_center_active
    n "Mr. Vance, listen to me, please—it wasn't her fault, I asked her to come up here, just let her go—"

    narrator "Until the boy spoke and tried to explain." #[cite: 4]

    show noah scared at stage_center
    show thomas angry at stage_right_active
    t "{size=+4}I DIDN'T GIVE YOU PERMISSION TO BREATHE ON MY LAND!{/size}"

    menu:
        "Throw yourself in front of Noah.":
            $ elena_humanity += 2
            $ elena_ruthlessness += 2
            show elena angry at stage_center_active with move
            show noah scared at stage_left with move
            e "Shoot me then, you drunken bastard! Go on! Pull the trigger on your own daughter!"
            narrator "Thomas doesn't hesitate. His left fist swings like an iron mallet, catching Elena across the jaw."
            with camera_shake
            narrator "She crashes into the straw, her vision exploding into white stars, tasting copper."

        "Scream for Noah to jump from the window.":
            $ trust_noah += 2
            show elena scared at stage_left_active
            e "NOAH, THE WINDOW! JUMP! GET OUT OF HERE!"
            show elena scared at stage_left
            show noah scared at stage_center_active
            n "I'm not leaving you with him! I'm not leaving you!"
            narrator "Noah steps forward, raising his hands, trying to put himself between the barrel and Elena."

    show thomas angry at stage_right_active
    narrator "Thomas shoulders the shotgun. His face is devoid of all humanity."
    narrator "He centers the bead directly between Noah's collarbones."

    with heavy_shake
    with gunshot_flash
    with red_flash

    narrator "{size=+12}BOOM.{/size}"
    
    narrator "But was shot to death there in front of her." #[cite: 4]

    scene bg_hayloft_night
    with slow_dissolve

    stop music fadeout 3.0

    narrator "The sound is not like a gun in the movies."
    narrator "It is an earthquake confined inside an oak room."
    narrator "The blue haze of burnt gunpowder hangs thick and suffocating, stinging the eyes and choking the throat."

    show thomas neutral at stage_right with dissolve
    show elena scared at stage_left with dissolve

    narrator "Noah is thrown backward into the hay bales."
    narrator "He doesn't groan. He doesn't thrash. His chest has simply ceased to exist."
    narrator "A wide, dark lake of crimson spreads silently through the chaff, soaking into the wood beneath."
    
    show prop_bloody_tickets at prop_examine 
    narrator "The Chicago bus tickets in his pocket are soaked through."
    hide prop_bloody_tickets with dissolve

    play music bgm_ruins fadein 3.0 

    show elena scared at stage_left_active
    e "Noah...?"
    e "{cps=15}Noah... please. Please get up. Noah...{/cps}"

    show elena scared at stage_left
    show thomas neutral at stage_right_active
    t "Dead. One less thief in the world."

    narrator "Thomas lowers the smoking barrel."
    narrator "He steps over Noah's body, his boots slipping slightly in the blood."
    narrator "He wraps his calloused hand into Elena's hair, dragging her violently to her feet."

    with camera_shake
    e "{size=+6}YOU KILLED HIM! YOU MONSTER! YOU MURDERED HIM!{/size}"

    show thomas angry at stage_right_active
    t "Shut up! You're coming to the house. You're going into the fruit cellar until I figure out which well to dump this carcass in."
    t "You made me do this! You brought this into my home!"

    scene bg_farmhouse_interior
    with cinematic_fade

    narrator "The father went away slurring, taking her away with him." #[cite: 4]
    narrator "He drags her through the mud, ignoring her kicks, her screams, her nails digging into his wrists."
    narrator "He throws her into the kitchen. Elena hits the table, knocking over empty beer bottles that shatter across the linoleum."
    
    narrator "Thomas slams the deadbolt and turns to the cupboard, grabbing a mason jar of moonshine to steady his trembling hands."

    show thomas thinking at right_talk with dissolve
    show elena tired at left_silent with dissolve

    t "He had it coming. Castle doctrine. Trespassers get shot."
    t "The sheriff will understand. Sheriff Miller owes me. Everyone in this county owes me."

    narrator "He turns his back to Elena, tipping the jar back and gulping down half the raw liquor, coughing as it burns down his throat."

    menu:
        "Smash a broken bottle across his neck and run.":
            $ elena_ruthlessness += 4
            narrator "Elena's grief mutates instantly into absolute, unadulterated hatred."
            narrator "She grabs the jagged neck of a broken beer bottle from the linoleum."
            narrator "With all the adrenaline surging in her veins, she lunges forward and rakes the glass across the back of Thomas's neck."
            with camera_shake
            t "{size=+4}ARGH! YOU BITCH!{/size}"
            narrator "Thomas stumbles into the counter, dropping the jar. Blood gushes down his collar, mixing with the spilled alcohol."
            narrator "He drops the shotgun to clutch his neck."

        "Sprint directly for the back screen door while he is drinking.":
            $ elena_humanity += 1
            narrator "Elena doesn't waste half a breath on revenge. Survival is the only instinct left."
            narrator "She kicks off from the floor and hurdles the broken glass."
            narrator "She slams her shoulder into the unlocked porch door, bursting through the screen mesh."

    scene bg_farm_exterior_night
    with heavy_shake

    narrator "After a lot of struggle, she managed to run from him." #[cite: 4]
    narrator "The October wind slaps her face as she bursts into the yard."
    narrator "Behind her, Thomas recovers."

    t "{size=+6}ELENA! STOP OR I SWEAR TO GOD I'LL DROP YOU WHERE YOU STAND!{/size}"

    scene bg_farm_field_night
    with quick_cut

    narrator "At the break of night she ran away, charging blindly into the black corn rows." #[cite: 4]
    narrator "She doesn't look back. She just runs."
    narrator "Mud sucks at her boots. The corn leaves slice at her cheeks like paper cuts."

    with heavy_shake
    with gunshot_flash
    with red_flash

    narrator "{size=+8}CRACK-THUMP.{/size}"

    narrator "A white-hot iron poker seems to drive directly through her right thigh."
    narrator "Elena screams as her leg folds beneath her, pitching her headfirst into the freezing loam."

    e "{size=+4}Aaaagh! God! God!{/size}"

    narrator "As she got shot in the leg." #[cite: 4]
    narrator "The buckshot has torn through the meat of her thigh. Blood, hot and slick, saturates her denim."
    narrator "Through the corn behind her, she hears Thomas's heavy boots slurring and slipping in the clay."

    t "Elena! I winged you! You can't outrun me on one leg, girl! Come back to the house!"

    narrator "Tears blinding her eyes, Elena forces herself onto her hands and knees."
    narrator "She crawls like a wounded animal into the tall grass. Then drags herself up against a wooden fence post."
    narrator "She scrambles over the barbed wire, leaving chunks of her flesh and denim on the barbs, and tumbles down the steep embankment toward the county road."

    scene bg_country_road_night
    with slow_dissolve

    narrator "Rain begins to fall, washing the mud and blood across the black asphalt."
    narrator "She limps, dragging her torn right leg, leaving a faint red streak behind her."
    narrator "Around the curve, the twin high-beams of an eighteen-wheeler illuminate the falling sleet."
    narrator "Elena throws her bloody arms up, staggering into the middle of the road, preferring death by steel than death by her father."
    narrator "The air brakes scream. The massive chrome grill stops inches from her face."
    narrator "The driver throws open the door. 'Jesus Christ, kid! Get in!'"

    jump act2_city_survival


# ===================================================================
# ACT II: THE ALLEY, THE NEEDLE, AND THE SYNDICATE
# ===================================================================

label act2_city_survival:
    scene bg_city_street_rainy_night
    with cinematic_fade

    stop music fadeout 2.0
    play music bgm_gloomy fadein 2.0 

    narrator "THREE DAYS LATER."
    narrator "Finally she reached a busy city away from those farms, and in that dreadful life." #[cite: 4]
    narrator "The trucker dropped her off at the edge of the industrial district, giving her twenty dollars and telling her to find a hospital."
    narrator "The city is an endless concrete labyrinth of steam vents, rain-slicked pavement, and absolute indifference."
    narrator "No one in this district looks at Elena Vance. They step over the homeless, ignore the bleeding, and keep their heads down."

    scene bg_city_street_daytime
    with slow_dissolve

    narrator "Daylight brings no warmth. The smog blocks out the sun."
    narrator "She roamed the streets as if looking for smth." #[cite: 4]
    narrator "Looking for a safe place. Looking for a reason to keep breathing."
    narrator "Her leg is swollen twice its normal size, throbbing with a sickly, feverish heat. Greenish-yellow bruising spreads from her knee to her hip."
    narrator "The lead pellets are still buried deep in the muscle of her thigh, poisoning her blood."
    narrator "If she goes to a public hospital, they will log the gunshot wound. They will notify the county sheriff. And Thomas Vance will know exactly where she is."

    scene bg_city_alley_night
    with slow_dissolve

    narrator "Night falls again. Sleet pools in the clogged gutters."
    narrator "And sat near an alley, trying to take out the bullet from her leg." #[cite: 4]
    narrator "She collapses behind a row of rusted grease dumpsters behind a Chinese restaurant."
    narrator "In her shaking hands, she holds a pocket knife she stole from a convenience store and a bottle of cheap 100-proof grain alcohol."

    show elena tired at center_solo with dissolve

    e "{cps=12}Do it. Do it or you die here in the garbage like a dog. Do it for Noah.{/cps}"

    menu:
        "Sterilize the blade with alcohol and dig the lead out cleanly.":
            $ elena_humanity += 2
            narrator "Elena pours half the liquor directly over the blade and the raw, torn wound."
            with camera_shake
            narrator "The agony is blinding. White light explodes behind her eyes as she sinks her teeth into her coat sleeve to muffle her own screams."
            narrator "With savage precision, she probes the torn muscle until the tip of the blade hits metal."
            narrator "{i}CLINK.{/i}"
            show prop_bullet at prop_examine 
            narrator "The flattened lead pellet pops out into her bloody palm."
            hide prop_bullet with dissolve
            narrator "She pours the rest of the alcohol into the open hole."

        "Bite down on your belt and rip it out in a fury of pain.":
            $ elena_ruthlessness += 2
            narrator "She doesn't wait for courage. Courage is for people with a future."
            narrator "She jams the blade straight into the puncture wound, twisting with pure venom."
            with heavy_shake
            narrator "A ragged scream tears through her lips as she gouges the lead free, tearing muscle and leaving the wound jagged and ragged."
            show prop_bullet at prop_examine 
            narrator "She looks at the bloody pellet of buckshot, then throws it into the slush."
            hide prop_bullet with dissolve

    narrator "Elena slumps back against the wet brick, drenched in cold sweat, her chest heaving as she tries not to vomit from the pain and shock."

    show elena tired at left_silent
    show mara neutral at right_talk with moveinright

    m "You got guts, kid. Or you're completely psychotic."

    narrator "Elena's hand snaps out instantly, pointing the bloody pocket knife toward the stranger's throat."

    show elena angry at left_talk
    show mara neutral at right_silent
    e "Stay back! Don't touch me! I'll cut you open!"

    show elena angry at left_silent
    show mara neutral at right_talk
    m "Easy with the toothpick. If I wanted you dead, I would've let the sepsis finish you by midnight."

    narrator "Tho the street was kinder to her and offered help but with a condition of loyalty." #[cite: 4]
    narrator "The woman steps into the dim sulfur light of the alley streetlamp."
    narrator "She is dressed in an oversized leather bomber jacket, a cigarette tucked behind her ear, her eyes calculating and completely devoid of fear."

    m "My name's Mara. I run errands for people who don't like dealing with banks or police."
    m "I saw you limping three blocks back. You took that slug out without passing out. That means you're tough, or you're running from something worse than dying."

    show elena tired at left_talk
    show mara neutral at right_silent
    e "What do you want?"

    show elena tired at left_silent
    show mara thinking at right_talk
    m "I need people who don't exist. People without IDs, without families, and without cold feet."
    m "I have an apartment with running hot water, penicillin, and clean gauze. But it comes with a price tag: absolute loyalty."
    m "You work my runs. You hold my packages. And you never ask who pays the bill. Deal?"

    menu:
        "Take Mara's hand and accept the syndicate life.":
            $ mara_bond += 2
            $ elena_ruthlessness += 1
            show elena neutral at left_talk
            show mara neutral at right_silent
            e "Deal. Just get me out of this rain before I bleed out on your shoes."
            narrator "Mara smiles grimly and pulls Elena to her feet."

        "Demand to know what kind of packages before agreeing.":
            $ elena_humanity += 1
            show elena thinking at left_talk
            show mara neutral at right_silent
            e "I'm not doing wet work for strangers. I'm not a killer."
            show elena thinking at left_silent
            show mara neutral at right_talk
            m "Nobody's asking you to shoot presidents, kid. Just moving contraband, cash, and packages. Now stand up before your leg locks up permanently."
            narrator "Elena hesitates, then nods, letting Mara help her up."

    jump act2_underworld_life


# ===================================================================
# ACT II PART 2: THE SYNDICATE & THE NUMBING HAZE
# ===================================================================

label act2_underworld_life:
    scene bg_maras_apartment
    with slow_dissolve

    narrator "TWO YEARS PASS."
    narrator "It wasn't easy, but time went on." #[cite: 4]
    narrator "Mara's apartment smells of stale tobacco, boiled cabbage, and damp carpet."
    narrator "Elena Vance learns the rhythms of the criminal underground. She learns that the city has its own pulse, driven by greed and desperation."
    
    show prop_briefcase at prop_examine 
    narrator "She carries locked briefcases through crowded subway cars. She collects envelopes from back-room bookies and illegal casinos."
    hide prop_briefcase with dissolve
    
    narrator "She learns how to walk without limping, even when the thick scar tissue on her thigh burns in the winter rain."

    show mara neutral at left_silent with dissolve
    show elena neutral at right_talk with dissolve

    narrator "But survival isn't the same as living."
    narrator "To keep the nightmares away—to silence the eternal sound of Noah's chest tearing open under Thomas's shotgun—she turns to what the street provides."
    narrator "And she got into drugs and addicts. Places she shouldn't have been into." #[cite: 4]
    narrator "Opium dens in the basement of laundromats. Pill mills run by disgraced doctors."

    menu:
        "Take the pills Mara leaves on the table to drown the memories.":
            $ addiction_level += 3
            $ elena_ruthlessness += 2
            scene bg_maras_apartment at bg_addiction_blur
            with dissolve
            narrator "Elena swallows the small white tablets dry."
            narrator "Within twenty minutes, the sharp edges of the world go soft and blurry. The constant adrenaline in her blood slows to a crawl."
            narrator "The ghost of Noah's face fades behind a thick, chemical fog."
            e "{size=-2}Good. Let it burn away. I don't want to feel anything. Feeling gets you killed.{/size}"

        "Rely on hard liquor and sheer hatred instead of pills.":
            $ elena_ruthlessness += 2
            $ elena_humanity += 1
            narrator "She pushes the pill bottle away, disgusted by the weakness it represents, and drains a glass of rye whiskey."
            narrator "The burning in her throat keeps her sharp, awake, and angry."
            e "{size=-2}I need to remember his face. Every line of it. I can't afford to go numb. If I go numb, he wins.{/size}"

    scene bg_bathroom_mirror
    with slow_dissolve

    narrator "One evening, before heading into the rain for a collection run, Elena stands before the cracked bathroom mirror."

    show elena tired at center_solo with dissolve

    narrator "It was a blur but too clearer than the past." #[cite: 4]
    narrator "She looks at her reflection."
    narrator "The nineteen-year-old girl who dreamed of writing stories in a Chicago attic is dead."
    narrator "Her cheekbones are sharp, her skin pale, her knuckles scarred from three separate back-alley brawls defending Mara's drops."
    
    show prop_gun at prop_examine 
    narrator "She wears a dark leather trench coat to hide the heavy .38 revolver she bought off a dockworker."
    hide prop_gun with dissolve
    
    narrator "And behind her eyes... she sees a cold, predatory gleam that chills her to the bone."

    e "{cps=15}You're looking more like him every day, Elena. You're becoming the monster.{/cps}"

    jump act3_first_kill


# ===================================================================
# ACT III: THE FIRST KILL & THE MONSTER AWAKENS
# ===================================================================

label act3_first_kill:
    scene bg_city_alley_night
    with slow_dissolve

    play music bgm_tension fadein 2.0 

    narrator "A Tuesday night. Sleet pelts the brickwork, freezing as it hits the ground."
    narrator "One night while getting into a fight on the street with someone..." #[cite: 4]
    
    show stranger angry at right_talk with moveinright
    show elena neutral at left_silent with dissolve

    man "You got five grand in that envelope, girl. Hand it over, or I'm taking it off your corpse."

    narrator "The man is one of Moretti's enforcers, a rival syndicate moving in on Mara's territory."

    show elena neutral at left_talk
    show stranger angry at right_silent
    e "This belongs to Mara. You touch this bag, and you won't live to spend it. Walk away."

    show elena neutral at left_silent
    show stranger angry at right_talk
    man "Mara isn't here to hold your hand, bitch! You're just a stray dog she picked up!"

    narrator "The man steps forward and strikes her across the face with his open palm."
    with camera_shake
    narrator "Elena's head snaps back against the damp brick. She tastes blood immediately."

    narrator "He lunges, pinning her shoulders to the wall, his face sneering down into hers."
    narrator "His breath smells of stale whiskey, rotting teeth, and tobacco."
    narrator "And then—the streetlamp above them flickers."

    # THE PSYCHOTIC FLASH
    scene bg_barn_interior_night
    show thomas angry at center_solo
    with quick_cut

    t "{size=+6}YOU BELONG TO ME, GIRL! YOU'RE MY PROPERTY!{/size}"

    scene bg_city_alley_night
    show stranger angry at right_talk
    show elena angry at left_silent
    with quick_cut

    narrator "She just remembered her father looking into the eyes of that somebody." #[cite: 4]
    narrator "The stranger's eyes become Thomas's eyes."
    narrator "The jawline. The cruel, tyrannical sneer."
    narrator "Every repressed horror of Vance Hollow detonates inside Elena's skull like high explosive."

    e "{size=+6}NO! NEVER AGAIN! GET OFF ME!{/size}"

    narrator "Her right hand slides down to the heavy bone-handled hunting knife she keeps sheathed in her boot."
    narrator "Before the man can even register the movement, Elena drives the six-inch steel blade upward under his sternum."
    
    with heavy_shake
    with red_flash

    man "{size=+4}Uggh... gh...{/size}"

    narrator "He stares at her, pupils dilating in absolute shock."
    narrator "She stabbed him to death." #[cite: 4]
    narrator "She doesn't stop. The rage is a physical entity taking control of her limbs."
    narrator "She rips the blade free and stabs him again. And again. And again."
    narrator "Four times. Five times. Seven times, driving the steel through his ribs."

    scene bg_city_alley_night
    with slow_dissolve

    narrator "The man collapses into the wet garbage, twitching once before going completely still."
    narrator "Rain washes the warm blood from Elena's face and hands."

    show elena angry at center_solo with dissolve

    narrator "For the first time in four years, the crushing weight in her chest vanishes."
    narrator "A dark, intoxicating warmth rushes through her veins. Power."
    narrator "Revenge took over her mind, the fights turned into murders." #[cite: 4]

    e "{cps=15}It was him. He's everywhere. The world is full of men just like him. And I'm going to kill every single one of them.{/cps}"

    jump act4_the_heist


# ===================================================================
# ACT IV: THE ARCHIVE HEIST & THE REVENGE WALL
# ===================================================================

label act4_the_heist:
    scene bg_city_street_rainy_night
    with cinematic_fade

    stop music fadeout 2.0
    play music bgm_ruins fadein 2.0 

    narrator "SEVEN MONTHS LATER."
    narrator "The state police believe there is a serial killer operating in the district."
    narrator "Three loan sharks, two abusive husbands, and a corrupt dock boss. All found in alleys with identical puncture wounds."
    narrator "But Elena has stopped hunting strangers. She is finally hunting the ghost that started it all."

    scene bg_city_alley_night
    with slow_dissolve
    
    narrator "1:00 AM. Behind the State Agricultural Archives building."
    narrator "Elena stands before the barred rear entrance. She has spent three weeks bribing a night janitor for the master key schedule and alarm bypass codes."
    
    show elena neutral at center_solo with dissolve

    e "He didn't just kill Noah. He killed Mom. I know he did. He said she ran away, but she left her coat. I just need the paper trail to prove he's a monster."

    menu:
        "Pick the rusty padlock on the basement grate.":
            $ investigation_progress += 2
            $ elena_humanity += 1
            narrator "Elena pulls two tension wrenches from her pocket, deciding to play it quiet."
            narrator "The lock is old, stiff with winter rust. She holds her breath, feeling the pins set one by one."
            narrator "{i}CLICK.{/i} The lock gives way. She slides the grate open and slips into the dark basement."
            
        "Smash the glass on the fire door and bypass the latch.":
            $ elena_ruthlessness += 2
            narrator "Patience is a luxury she no longer possesses."
            narrator "Elena wraps her coat tightly around her elbow and drives it through the reinforced wire glass."
            with camera_shake
            narrator "The shattering sound echoes down the alley. She ignores it, reaching through the jagged hole and hitting the crash bar."
            
    scene black
    with quick_cut

    narrator "Inside the pitch-black archives, the smell of decaying paper and mothballs chokes the air."
    
    show prop_torch at prop_floating 
    narrator "She clicks on a small penlight. Rows of green steel filing cabinets stretch endlessly into the darkness."

    e "Vance Hollow... 1980 to 1995. Section H."

    narrator "She scans the aisles, her flashlight beam cutting through the dust."
    narrator "She finds the drawer marked {i}Agricultural Subsidies & Placements{/i}."
    
    show prop_files at prop_examine 
    narrator "She rifles through the manila folders, her heart hammering against her ribs, until she finds the name: {b}VANCE, THOMAS.{/b}"
    hide prop_files with dissolve
    hide prop_torch with dissolve

    scene bg_revenge_wall_apartment
    with cinematic_fade

    narrator "By 4:00 AM, the stolen documents are pinned to the plaster wall of her apartment's spare room."
    
    show elena angry at center_solo with dissolve
    
    show prop_yarn at prop_ui_corner 
    show prop_photos at prop_examine 
    show prop_pins at prop_floating 

    narrator "Across the entire wall, hundreds of documents, old black-and-white photos, and coroner reports are linked by taut red yarn."
    narrator "And at the core of the web lies the secret she unearthed."

    hide prop_photos
    hide prop_pins
    hide prop_yarn
    with dissolve

    e "Thomas didn't just murder Noah."

    show prop_report at prop_examine 
    narrator "She reads the stolen state reports aloud into the dim room, her voice shaking with rage:"
    narrator "{i}'1988: State Foster Care Placement Program — Vance Farm Agricultural Apprenticeship.'{/i}"
    narrator "Three state wards sent to work the farm under Thomas's care. All three reported as 'runaways' within two years. None ever found."
    narrator "And her mother—who Thomas claimed 'abandoned the family for a trucker'—never withdrew a single cent from her savings account."
    hide prop_report with dissolve

    $ learned_orphan_secret = True

    e "The orchard. The apple orchard on the ridge. The soil was always turned there."
    e "He buried them all under the apple orchard."
    e "Where all those orphans died, her mother, and her lover." #[cite: 4]
    e "And the whole county looked the other way because he controlled the grain co-op and paid off the sheriff."

    show mara nervous at left_talk with moveinleft
    show elena angry at right_silent with move

    m "Elena. Look at this room. Look at yourself. You're losing your mind."

    show elena angry at right_talk
    show mara nervous at left_silent
    e "I'm not losing my mind, Mara. For the first time in twenty-four years, I see everything perfectly clearly."

    show elena angry at right_silent
    show mara nervous at left_talk
    m "You've got five murders on your ledger in this city alone. The precinct is setting up a special task force."
    m "If you go back to that county, you won't survive the week. Thomas will kill you, or the cops will catch you."

    show elena angry at right_talk
    show mara nervous at left_silent
    e "I don't plan on surviving the week, Mara. I plan on settling the balance."

    menu:
        "Say goodbye to Mara with genuine gratitude for saving your life.":
            $ elena_humanity += 3
            show elena tired at right_talk
            show mara nervous at left_silent
            e "You took me in when I was bleeding to death in the trash. I never thanked you for that, Mara. You're the only family I have left."
            show elena tired at right_silent
            show mara thinking at left_talk
            m "Don't get sentimental on me, kid. Just... try not to let that old bastard take you down with him."

        "Coldly dismiss her and pack your revolver.":
            $ elena_ruthlessness += 3
            show elena angry at right_talk
            show mara nervous at left_silent
            e "Stay out of my way, Mara. This isn't syndicate business. This was always how it had to end."
            m "You're a dead woman walking, Vance."

    jump act5_the_return


# ===================================================================
# ACT V: RETURN TO VANCE HOLLOW
# ===================================================================

label act5_the_return:
    scene bg_country_road_night
    with cinematic_fade

    stop music fadeout 2.0
    play music bgm_gloomy fadein 2.0 

    narrator "FOUR YEARS TO THE NIGHT."
    narrator "The midnight greyhound bus deposits Elena Vance at the abandoned crossroad, groaning as it pulls away."
    narrator "The air smells identical to the night Noah died: wet soil, decaying timber, and sulfur."
    
    show prop_gun at prop_examine 
    narrator "Inside her heavy wool coat rests a Smith & Wesson .38 Special, loaded with five hollow-point cartridges."
    hide prop_gun with dissolve

    scene bg_farm_field_night
    with slow_dissolve

    narrator "And one night she came across the same farm from 4 years ago." #[cite: 4]
    narrator "Where all happened. Where all those orphans died, her mother, and her lover." #[cite: 4]
    
    narrator "She steps over the split-rail fence she once scrambled across with Noah."
    narrator "The corn is standing tall again—brown, dry, and whispering in the autumn breeze like a chorus of the dead."

    if addiction_level > 2:
        narrator "Her hands tremble slightly, craving the chemical numbness of the pills, but she forces the withdrawal down. She needs to be sharp."
    
    narrator "She walks past the darkened farmhouse."
    narrator "She passes the apple orchard on the ridge. She pauses, looking at the gnarled roots. Beneath them sleep the lost orphans, her mother, and the boy who bought bus tickets to Chicago."

    narrator "No light shines in the second-floor window of the house tonight."
    narrator "Instead, a faint, sickly yellow lantern glow leaks through the high loft slats of the barn."

    scene bg_barn_exterior_night
    with dissolve

    narrator "The barn waits for her. A monolith of trauma."
    narrator "The large double doors are chained open, welcoming her in."

    scene bg_barn_interior_night
    with slow_dissolve

    narrator "Elena steps into the lower bay. The smell of machine grease and old hay hits her."
    narrator "The floorboards still bear the faint, scrubbed stain where Noah's blood drank into the wood."
    narrator "She went in the same hayloft." #[cite: 4]
    narrator "She climbs the ladder, rung by agonizing rung."

    jump act5_the_confrontation


# ===================================================================
# CLIMAX: THE FINAL HAYLOFT
# ===================================================================

label act5_the_confrontation:
    scene bg_hayloft_night
    with slow_dissolve

    play music bgm_tension fadein 2.0 

    narrator "She reaches the top deck."
    narrator "And luckily there he was, standing there looking at the barn." #[cite: 4]

    show thomas thinking at right_silent with dissolve

    narrator "Thomas Vance is older, withered by whiskey and liver failure, his hair snow-white."
    narrator "He is wearing the exact same grease-stained coat."
    narrator "Leaning against the timber post beside him is the 12-gauge shotgun."

    narrator "As he turned to look behind and saw her..." #[cite: 4]

    show thomas neutral at right_talk
    t "Took you long enough, Elena."

    show elena angry at left_talk with moveinleft
    show thomas neutral at right_silent
    e "You knew I was coming."

    show elena angry at left_silent
    show thomas thinking at right_talk
    t "The whole state knows about the girl leaving bodies in city alleys."
    t "I read the papers. I recognized the handiwork. You always had my temper."
    t "I told you that night—you're my blood. You can't outrun what you're made of."

    show elena angry at left_talk
    show thomas thinking at right_silent
    e "I'm not your blood. I'm your executioner."
    e "I found the files on the foster children, Thomas. I saw the records. I know what's buried under the orchard."
    e "I know about Mom."

    show elena angry at left_silent
    show thomas angry at right_talk
    t "They were ungrateful vermin! All of them! Just like that city boy!"
    t "They wanted to take what was mine! This land is mine! I fed them, and they tried to run!"

    show prop_gun at prop_examine 
    narrator "Elena draws the .38 revolver, cocking the hammer with a sharp click."
    narrator "She aims it straight between his eyes."
    hide prop_gun with dissolve

    show elena angry at left_talk
    show thomas angry at right_silent
    e "Four years ago, you shot Noah right where you're standing."
    e "You took everything from me. Now it's time to pay the bill."

    show thomas neutral at right_talk
    t "Go ahead then. Shoot your old man. Pull the hammer. Prove that everything I taught you was right."
    t "If you kill me, you just prove you're exactly like me."

    # ===============================================================
    # THE ULTIMATE BRANCHING DECISION
    # ===============================================================

    menu:
        "Fulfill the tragedy: Shoot him 4 times, then use the last bullet on yourself.":
            jump ending_original_hayloft_tragedy

        "Execute Thomas, burn the barn to the ground, and vanish into the underworld." if elena_ruthlessness >= 4:
            jump ending_ashes_and_shadow

        "Break the cycle: Lower the weapon, expose his crimes to the law, and walk into the dawn." if elena_humanity >= 4:
            jump ending_the_new_dawn


# ===================================================================
# ENDING 1: THE CANON ORIGINAL TRAGEDY (MURDER-SUICIDE)
# ===================================================================

label ending_original_hayloft_tragedy:
    narrator "Elena doesn't blink."
    narrator "Her finger pulls the double-action trigger."

    # SHOT 1
    with heavy_shake
    with gunshot_flash
    with red_flash
    narrator "{size=+10}BANG!{/size}"
    show thomas surprised at right_silent
    narrator "The first bullet tears into Thomas's right shoulder, spinning him into the hay bale."

    # SHOT 2
    with heavy_shake
    with gunshot_flash
    with red_flash
    narrator "{size=+10}BANG!{/size}"
    narrator "The second bullet punches through his abdomen. He gasps, collapsing onto his knees."
    t "Elena... wait..."

    # SHOT 3
    with heavy_shake
    with gunshot_flash
    with red_flash
    narrator "{size=+10}BANG!{/size}"
    narrator "The third bullet shatters his collarbone, driving him flat onto the straw."

    # SHOT 4
    with heavy_shake
    with gunshot_flash
    with red_flash
    narrator "{size=+12}BANG!{/size}"
    narrator "She shot him all 4 times until there was no sound." #[cite: 4]

    scene bg_hayloft_night
    with slow_dissolve

    stop music fadeout 3.0
    play music bgm_ruins fadein 2.0 

    narrator "Four shots."
    narrator "Until there is no sound left in the world."
    narrator "Only the smell of cordite, blood, and cold rain."

    show elena tired at center_solo with dissolve

    narrator "Elena stands over her father's corpse."
    narrator "She looks at her shaking hands. Her hands are covered in his blood. Her blood."
    narrator "The revenge is complete. But there is no peace. No Chicago. No laughter. No Noah."
    narrator "She has become the very demon she came to slay. The farm has finally consumed her entirely."

    e "{cps=12}Noah... I promised I'd never live in this dirt again.{/cps}"

    show prop_gun at prop_examine 
    narrator "She raises the revolver to her own temple. The steel is freezing against her skin."
    narrator "One cartridge remains in the cylinder."
    narrator "Elena closes her eyes and pulls the trigger."
    hide prop_gun with dissolve

    with heavy_shake
    with gunshot_flash
    with red_flash

    narrator "{size=+14}CLICK-BOOM.{/size}"
    narrator "And with the last one killed herself too." #[cite: 4]

    scene bg_hayloft_dawn
    with cinematic_fade

    narrator "Dawn breaks over Vance Hollow."
    narrator "The golden light filters through the loft rafters, touching two bodies lying cold in the straw."
    narrator "The farm remembered everything."
    narrator "And finally, the hollow was silent."

    centered "{size=+26}ENDING 1: HAYLOFT (CANON TRAGEDY){/size}\n\n{i}She shot him all 4 times until there was no sound.\nAnd with the last one killed herself too.{/i}" #[cite: 4]
    pause 5.0
    return


# ===================================================================
# ENDING 2: ASHES AND SHADOW (THE CRIME LORD)
# ===================================================================

label ending_ashes_and_shadow:
    with heavy_shake
    with gunshot_flash
    with red_flash
    narrator "{size=+10}BANG! BANG! BANG! BANG!{/size}"

    show thomas surprised at right_silent
    narrator "She shot him all 4 times until there was no sound." #[cite: 4]
    narrator "Thomas collapses lifeless into the straw, the blood pooling beneath his chest."

    show elena angry at center_solo with dissolve

    e "Burn in hell with this rotten farm."

    narrator "Elena kicks over the kerosene lantern."
    narrator "Flames greedily lick across the dry timothy straw, exploding upward into the dry pine rafters."
    narrator "The old wood catches instantly."

    scene bg_barn_exterior_night
    with flash
    
    stop music fadeout 2.0
    play music bgm_gloomy fadein 2.0 

    narrator "Elena walks down the gravel drive as an eighty-foot wall of fire consumes the barn."
    narrator "The heat warms her scarred face. The ghosts of Vance Hollow are reduced to ash."
    narrator "She doesn't stay to watch it burn to the foundations."

    scene bg_city_street_rainy_night
    with cinematic_fade

    narrator "She returns to the city that made her."
    narrator "Elena Vance never looked back, reigning in the shadows of the metropolis with an iron grip."
    narrator "She becomes Mara's partner, running the district with a brutality that terrifies even Moretti's men."

    centered "{size=+26}ENDING 2: THE ASHES OF VANCE HOLLOW{/size}\n\n{i}Some fire cleanses.\nSome fire simply leaves you with a blackened soul.{/i}"
    pause 5.0
    return


# ===================================================================
# ENDING 3: THE NEW DAWN (REDEMPTION & TRUTH)
# ===================================================================

label ending_the_new_dawn:
    show elena tired at left_talk
    show thomas thinking at right_silent

    narrator "Elena's thumb slowly eases the revolver's hammer back into resting position."

    e "No."

    show thomas surprised at right_talk
    t "What are you doing? Pull the trigger! Prove who you are!"

    show elena neutral at left_talk
    e "I know who I am. I'm Elena. And I will never let you turn me into you."

    show prop_report at prop_examine 
    narrator "She takes the handwritten ledger of his crimes, throws it at his feet, and levels the weapon at his kneecap."
    hide prop_report with dissolve

    with heavy_shake
    with gunshot_flash
    narrator "{size=+8}BANG!{/size}"

    t "{size=+6}ARGHHH! MY LEG!{/size}"

    narrator "Thomas collapses, writhing in agony."
    e "Now you know how it feels to crawl through the mud, old man."
    e "The State Bureau of Investigation already has copies of your burial records. I mailed them before I got on the bus."
    e "They're coming down the road right now."

    scene bg_hayloft_dawn
    with slow_dissolve

    stop music fadeout 3.0

    narrator "Morning sun spills through the barn slats, bathing the loft in pure amber light."
    narrator "Elena turns her back on the groaning monster and descends the ladder into the fresh air."

    scene bg_farm_exterior_dawn
    with slow_dissolve

    show elena happy at center_solo with dissolve

    narrator "Sirens wail in the far distance, approaching the Vance Hollow bridge."
    narrator "Elena Vance walks past the split-rail fence onto the state highway."
    narrator "She drops the revolver into the roadside creek, letting the cold water wash the soot from her palms."
    narrator "Noah's promise was finally kept."
    narrator "She was leaving. And she would never, ever return."

    centered "{size=+26}ENDING 3: THE MORNING PROMISE{/size}\n\n{i}Some places remember.\nBut you don't have to live there forever.{/i}"
    pause 5.0
    return