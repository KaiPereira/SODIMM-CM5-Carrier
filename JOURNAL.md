---
title: Cluster Board
author: Kai Pereira
description: An open source 8 node ITX cluster board running custom compute modules, supports up to 256 GB of ram
created_at: 2025-08-14
---
## Day 1 - Research Galore - 6 Hours

Recently, I came across a video from one of my favorite content creators, [Bitluni](https://www.youtube.com/@bitluni) about building a Risc-V supercluster. This was one of the coolest concepts I've ever seen in my life, combining the power of 100's of micro controllers to create a decently powerful system.

![Pasted image 20250815210804.png](journal/Pasted%20image%2020250815210804.png)

But then I thought to myself, what if we scaled this up, what if we went BIG.

I started doing some research on cluster boards and how they actually work. I noticed that Bitluni's board was very similar to my Cheetah MX4, 3DP motherboard, so knowing that I kind of had some previous knowledge to what I was looking into, really helped alot!

I figured out that Bitluni basically had this cluster board, and then on that cluster board, it had these connectors called PCIe which allowed fast data transfer but also to basically plug in cards to your board like a PC.

This was such a cool concept, creating a cluster of computers that acted as a swarm, from basically many mini computers, I had to make one too.

You already know how I function though, I needed to go a bit bigger than Bitluni so I started researching about cluster boards, specifically CM4 cluster boards. Basically, rasp pi makes these things called "pi compute modules" (CMx) which can basically plug into these types of motherboards using PCIe or other connectors to turn their plain PCB, into a devboard of sorts with extra features on the cluster board.

Jeff Geerling is a really interesting guy I came across who loves messing around with cluster boards like this, I'd highly suggest checking out his stuff and learning how it all works https://www.jeffgeerling.com/

Anyways, I kind of know exactly what I want to make now, a cluster board with custom compute modules for maximum power, it takes a bit of time to wrap your head around this concept of PCB's on PCB's but it's really cool. I also kind of want to go overkill, I never like making stuff that the ordinary person would make, so something that sounds impressive, like 100's of gb's of ram, or 100's of gpu's, just the wow factor.

I was on a plane basically doing all this research, so it gave me a solid 6 hours of time on research what exactly a cluster board is and how everything works, but I've only just scratched the surface.

## Day 2 - Linux, linux and linux - 8 Hours

Before I wanted to dive more into this project, I wanted to understand some of the software behind what I'm actually doing. I came across this insanely cool resource called https://www.thirtythreeforty.net/series/mastering-embedded-linux/ which teaches Linux embedded systems from a very high level standpoint.

The reason I wanted to look into this, is to understand what goes into making a compute module. You see, you need the RAM, storage, boot ROM, SoC and peripherals to make the board, like USB, UART, SPI, ADC, etc. All the basically combined to form a compute module.

![Pasted image 20250815210554.png](journal/Pasted%20image%2020250815210554.png)

On the software side, it looks something like the bootloader -> linux -> the ssh server, web server, interface, programs anything the user can interact with or run on. So you basically boot your device into linux, and then you can interact with the miniature filesystem that you have access to, it's like a mini computer.

![Pasted image 20250815210615.png](journal/Pasted%20image%2020250815210615.png)

Now you're probably wondering, what's an SoC... SoC stands for System on Chip, it's basically a complete system squeezed onto a tiny piece of silicon. On the SoC, you'll find:
- The CPU
- Sometimes accelerators like an NPU, GPU, DSP, etc.
- I/O controllers
- Peripherals
- Sometimes other things like bluetooth/wifi, security, an SoC can have *anything*

But anyways, let's go over some of the core parts...

The CPU is the brain of the SoC, I could talk for years about how the CPU works, but it basically executes the instructions of your programs.

The accelerators are specialized parts of the chips that are really good at specific things like training AI, or math, for example, a GPU is really good at math and AI, a DSP is really good at audio acceleration, there's so many different types of accelerators.

The I/O controllers handle like the different communication protocols like USB, ethernet, PCIe, etc. Just internal data flow in general, transferring information to and from inside the SoC.

The peripherals actually do something, produce sound, display stuff, control motors, etc. They're GPIO's, ADC's, DAC's, PWM controllers, everything that controls stuff.

And then sometimes chips have some other cool things like wifi/bluetooth, these are just other little "blocks" of hardware inside of the SoC that does stuff.

We've only talked about INSIDE of the SoC thought, what about outside of it?

Let's talk about the SoM, the System on Module.... This is basically those compute modules I was talking about, those are SoM's. When you add RAM to the outside of your SoC, that's part of the SoM, so what are all the things you need on the SoM.

The SoM will typically have RAM, the SoC, storage, power management, clocking, connectors, everything that you would find on a pi compute module persay. It turns the little SoC complete system, into a full computer ready to run programs, operating systems, anything your heart desires.

Now lots of people are probably wondering what RAM actually is.. It's basically like storage for the data and instructions that the SoC is actively using, so more RAM is more computational power!

The storage is long term memory (while RAM is short term), it'll hold the operating system, programs, data, everything. Sometimes there's a thing called the bootloader, which is a small program that runs when the SoM turns on, it's sometimes stored in the storage or sometimes in the SoC.

Power management is another things that's really important. The cluster board get's a primary voltage of like 12 - 48V, and you need to regulate it down for the SoC, RAM, peripherals, etc. All the different parts have different voltage requirements so you have to properly regulate the voltage and distribute it to the components on the compute module. You'll also usually want monitoring or power protection, just to make sure you don't actually ruin a component on the board.

And finally, there's all those extra parts on the board like the clock, connectors, etc. The clock is usually pretty important because it makes sure that everything is working in unison together. Think of it like an orchestra, it would be the conductor, it's very important to have a crystal for things like external connectors where data needs to leave the SoC at proper intervals, and generally just the SoC to make sure everything's working right. 

And then there's the connectors, depending on what you make, you'll need more or less, I'm making compute modules so I don't actually need like USB or ethernet ports or anything on the actual card, I just need PCIe lanes where all the information from the motherboard will travel to the cards, think of it like a really big connectors that everything will travel through. This makes it very modular, and very fast, because it goes directly to the motherboard. You can also put like debugging headers on the compute module to make sure that each card is working properly, I'll decide on this later.

Anyways, I spent a REALLY long time writing this, it helps me solidify the information of what I've learned so it's helpful for me too. This is just the start to how the board will work though, what I've described is just how the computational modules will work, we haven't even gotten to the motherboard yet. This should give a solid understanding to how the hardware to work, and I've given a brief overview of the software which is also quite interesting!

Once you start looking at many linux capable boards, you'll start to see the patterns:

![Pasted image 20250815210716.png](journal/Pasted%20image%2020250815210716.png)

I've also learned quite a bit more than what I've described, like a high level overview of the software and potential part choices, but I'll save that for when I have a better idea.

## Day 3 - Rise of the Turing Pi - 8 Hours

While doing all this research, I came across a board that Jeff Geerling had tried out. It was basically what I was trying to make, a 4-node ITX motherboard that supports up to 128gb of ram and each compute module supported up to 6 TOPS of NPU performance using their RK1 board, this was the turing pi 2 https://turingpi.com/product/turing-pi-2-5/ . This is going to be one of the core motivations for my project, to make something *better* than this board. 

![Pasted image 20250815211305.png](journal/Pasted%20image%2020250815211305.png)

The turing pi provides a really good core concept of what you need on a cluster board:
- Ethernet
- BMC controller
- GbE switch
- Mini PCIe express slots
- DSI and HDMI
- USB
- SATA and M.2 ports
- Breakout GPIO's
- Power of course
- SIM slot
- And then the 4 node modules

![Pasted image 20250815210117.png](journal/Pasted%20image%2020250815210117.png)

These are kind of the core things you need on a cluster motherboard, and actually a computer motherboard in general, with a few alterations, you could turn this cluster board into a desktop computer motherboard, but that's NO FUN!

On a cluster board, there's usually 2 ethernet ports, one to communicate internally, and one to communicate externally. The external ethernet usually acts as an uplink which you can wire to the internet or a router or something to communicate with it. The internet one acts as the cluster fabric that you could wire up to another motherboard (so 2 motherboards attached) to act as basically another cluster, isn't that so cool! So you could create clusters on clusters of these boards!!!

The BMC controller is basically the parent to the compute modules, it helps manage power, monitor, network, etc. It can basically control and monitor your entire cluster. It's usually a dedicated MCU that's always powered on and basically babysits the compute modules.

The GbE switch is incredibly important, it basically connects all the compute modules together so that they can act as one. It handles the switching between compute modules and aggregates all the traffic from every node.

The Mini PCIe express slots basically act as extra nodes for the board for adding extra capabilities that the normal compute modules don't have. For example, you could add dedicated accelerator cards, modems, storage, anything that supports mini PCIe and that you've implemented on your board. It's really cool!

The DSI/HDMI is fairly simple, it basically just lets you hook up a monitor to your SoM so that you can interface graphically with your board. They're not actually necessary, but they're really useful if you don't want to just communicate to your board via other connectors.

The extra USB's on the board are for really anything that is supported. Whether that's keyboards, mice, external storages, you pretty much know the geist, anything that you would plug into your own laptop that's supported. You really have to take into account the protocols your SoC/MCU supports just to make sure that you could add things like extra external storage. Typically, you usually have one USB per node and each node can kind of act as it's own device, very neat stuff! Sometimes you'll also have like a USB-C port on your board too which provides enough power to not run the entire motherboard, but to just program it.

Next up is the SATA and M.2 ports. You might've heard of these if you've ever built a computer before, they let you interface with things like HDD's, SSD's, wifi sometimes using a specific connector cable. They're easy ways of opening up more features to the user.

The breakout GPIO's are basically extra I/O headers that are on the board if you want to add whatever hardware your heart desires. Sensors, LED's, UART, PWM, whatever you want, you can think of them like the GPIO's on the Rasp Pi 5, they're just general I/O pins that allow flexibility and customization of your motherboard.

Then we have the power, it's pretty straightforward, it's just usually a single DC input that's distributed to all the modules, sometimes stepped down or buck converted.

Sometimes you'll find a SIM slot on a motherboard. It gives your board cellular network connectivity that's useful when you don't have wired internet. It's just like the SIM slot on your phone and will typically be connected to a mini PCIe modem card.

Boards will also usually have an SD Card slot that will act as additional storage so you could like run different operating systems if you want and to quickly change stuff up. You'll find that's it's often times on the bottom, this is because it takes up lots of space but isn't actually required for the board to function, so you can kind of just solder it on the board if you really want it, it's not necessary though.

And then of course you'll have the SoM's/nodes on your board. These are usually connected via backplane or mezzanine connectors like PCIe, and you can like stack them on the board to get more or less power/features. This is the core concept of our board.

You'll hear me use the words backplane and mezzanine, they are **structural** components on a board, basically giving it another dimension. This allows you to increase circuit density, it's insanely interesting and works very well!

![Pasted image 20250815210344.png](journal/Pasted%20image%2020250815210344.png)

Anyways, I now have a really strong overview of what I'm actually making from a high level standpoint and I hope that you've also learned something from all my talking! It takes me a really long time to gather all this information, but it's insanely cool once you understand it.

I'm now confident enough to start picking out some components for my board and getting more into the exact specifics of what I want to build.

## Day 4 - Parts and specifics :D - 10 Hours

Now that I've learned about pretty much everything that you actually have on a cluster board and compute module, it's time to think more about the specifics of the actual board I'm going to make.

I'm going to start off with designing the compute module because it's easy to just produce and then test out quickly which is very convenient, you kind of need the compute modules for the motherboard too, so I think it's the right thing to start with.

Anyways the first thing I have to do for designing my SoM (compute module) is choosing an SoC. Now I have a couple SoC's I've had my eye on while researching. Notably:
- RP2350 - Cheap, decently powerful, all around
- Rockchip RK3588 - Moderately expensive, insanely powerful, many good features
- Intel N100 - Moderately expensive, hard to integrate but powerful, windows support
- NXP i.MX 8M Plus - Moderately expensive, reliable and decently powerful
- NVIDIA Jetson Orin - EXPENSIVE, insanely powerful GPU capabilities meant more for cluster
- WCH CH32V003 - Dirt cheap, risc-v, good for a silly 256 core+ project

Honestly the RP2350 probably shoudn't even be on this list, but it was the first thing I thought of for this project. I also thought that a cheap CH32V003 chip would be fun like the one Bitluni did to maybe get like over 100, maybe even 1000, but it's not really the type of project I want to make.

Overall I kind of want to go with the Rockchip RK3588, it's insanely powerful, a bit pricy, but perfect in my opinion for this board. It's the same chip the Turing RK1 used,  and I think it's a very good option.

I also want to support maybe some other types of cards for this board like the NVIDIA Jetson Orin, but not design the SoM, just buy one.

Now let's take a quick look at the RK3588, it doesn't have many docs, but it's really cool:
- Octo-core CPU, insane for multithreading and pure power
- Low power control which is very helpful for a motherboard if you want sleep states persay
- ARM Mali-G610 MC4 GPU with 4 shader cores, which will give some good acceleration for mathematics and stuff
- 6 TOPS of performance on the NPU, which will honestly be a standout feature, because you'll be able to run large AI training on the cluster which is really cool.
- 64 Bit LPDDR4/LPDDR5 memory which is insanely cool, because you could design for insanely powerful DDR5 ram, but I'll probably just stick with DDR4.
- eMMC which is basically soldered down storage and is up to 10x faster than SD cards. It's also more compact and works alongside SSD's and drives
- Up to 8K at 60Hz and dual display which is really good for multi media, so I'll definitely add HDMI
- 48 mega pixels ISP per camera input which gives it really powerful computer features
- Some good audio interfaces, I won't really go into it
- High speed dual USB 3.1 and other interface connection support
- Some good security features

I wrote all of this by hand which took a long time... But you can tell that this SoC is a beast for around just $50, so while the compute modules will probably be over $100 each, it'll be insanely powerful.

Now that I've chosen my SoC, I want to look into all the parts on the SoM again and just choose what I want to focus on. So on the SoM I need:
- RAM - LPDDR4/5
- eMMC
- Power management - I think there's actually like a specific IC for this
- Debugging - Maybe some headers to interact with the compute module without PCIe
- PCIe interface - The main connector to the motherboard backplane
- Networking - GbE phy, I'll explain this soon

Now the first thing I learned while making this list was the GbE Phy which is basically the physical ethernet layer and can transfer data at 1 GB/s, it's needed for ethernet. 

The second thing I learned was that there's a dedicated power management module called the PMIC (power management IC). It's basically many buck converters and LDO's on one chips and handles the power rails, sequencing and voltage for the board.

The first thing I kind of want to focus on for the SoM is the RAM. Now I could support LPDDR5, but it's really just overkill and not needed, so I'll just go with the LPDDR4 because it's cheaper.

Now it's actually a bit hard to find LPDDR4 RAM, JCLCPB is almost all out of LPDDR4 specifically, but I kind of want to source it from their parts library so I can get PCBA and not have to reflow BGA or anything like that...

I did find 32 Gb's of LPDDR4 on JLCPCB for $110 in the form of 16, 2Gb chips, but that's a tad expensive and I feel like I could get it lower. But the advantages of this, is I could just get PCBA, but 16 ram chips is absolutely absurd.

Anyways I asked on the KiCad discord server for some help after this finding RAM and how complicated of a project this would be and figured out that I was in for a bit of a treat. I was informed that with all the absolute insane amount of connections I had, and the BGA parts, I'd need 10 layer HDI, which would cost around $1000 for just the boards, and I'd also need insanely good impedance control. And this isn't even counting the fact that you still need to get the schematic perfectly right, and get all the PCB's assembled, so you're looking at almost $2000, just for a chance that it works.

So for now, I'm going to focus my attention on building the cluster board, because I think I'll actually learn more building that and it's also not as complicated or as expensive, but still pretty darn hard.

## Day 5 - Let's build a cluster board

Now that I've postponed my compute module shenanigans, I want to focus my attention on building the cluster board.

Now I've already gone over what you actually need for a cluster board, so let's go over the specs of MY cluster board I want to build.

Now building a board exactly like the Turing Pi 2 is actually insanely hard, this is because the Turing Pi 2 has LOTS of high speed traces because it uses PCIe for stuff like NVMe storage but I can just skip this stuff and just use like SD cards or something else.

I kind of want to model this board similar to the DeskPi Super6C but I want to include a BMC and maybe like an ethernet switch and potentially like PCIe for network cards or something, but I have to look into it a bit more.

![Pasted image 20250830224212.png](journal/Pasted%20image%2020250830224212.png)

**So here's what the board is going to look like:**

There's going to be 4 - 8 **vertical** mezzanine connectors (like the turing pi 2) with daughter cards, this makes everything a bit more expensive, but modular and it's a good intro before tackling this project. Also that means if the mainboard works but not the daughter cards, it's less expensive than just re-doing the entire board. This also means I can get 2 separate grants for my project so it'll cost me less to make!

A small BMC to control power, a small USB mux to communicate to individual modules and communication over ethernet. And maybe I'll use an esp-32 or something so it can have a web UI!

12/24V PSU through a barrel jack or an ATX connector, not quite sure which one yet, so it's easy to power with enough juice.

An ethernet switch with 4 - 8 downlinks and then 2 uplinks for the networking. This allows me to control lots of modules and actually stack the modules to make a super-cluster.

Fan headers so you can power fans to each module for cooling and maybe an RTC battery to help maintain the clock on the mainboard.

Per NVMe SSD storage, this isn't too much more complicated to add but I think it's pretty useful and important to have.

USB, HDMI and micro-USB. The micro-USB is for flashing, the USB is for peripherals and the HDMI is for video output!

And just like that, we pretty much have our entire board layed out. Tomorrow I want to research a bit more how the daughter card will work, and actually get started working on it.

## Day 6 - The daughter board - 5 Hours

Now the first thing we have to do before making the board, is creating daughter boards for all the compute modules. I'm focused on just making daughter cards for the CM4 and the CM5 so that's going to be my main focus.

![Pasted image 20250830224046.png](journal/Pasted%20image%2020250830224046.png)

Now the CM5 is pretty much a drop-in replacement for the CM4 so I don't need to design in anything extra other than just taking into account the extra power that the CM5 needs.

So now let's talk about what the daughter card actually needs on it.

So the first thing you need is the mezzanine connectors to attach the compute module to the daughter card, and the daughter card to the motherboard. It's also important that you have mechanical supports for the card so you don't damage it during insertion or replacement.

Next you need the power management, you need 3.3V and 5V, the 3.3V is for the NVMe SSD and the 5V is for the compute module.

Then you need your storage. This is eMMC, SD card or even both if you want. Personally I'm probably going to support both because it just adds rigidity to the board in case anything fails!

And then you just really need to break out what pins you want. This is like breaking out USB, UARD, Gigabit Ethernet and the NVMe storage and other stuff you want! The NVMe storage is a bit trickier than the others because if you break it out through the backplane connector, you need to manage the tricky high speed signals, or you can just break it out as a connector on the actual daughter card. If you break it out through the backplane, you can actually pool the storage which is cool, but it's way more complicated, so I'm just going to stick with a connector on the actual carrier.

And then you need the extra things on your board too like:
- the fan header, this is just a connector on the board for each fan to connect to the daughter card
- LED's and stuff for power and debugging, just kind of nice to have
- UART and JTAG headers for debugging
- Expose GPIO headers, I'll decide if I want to do this later but it's good if you want to add extra hardware to the daughter card which can be handy

And just like that, we've pretty much figured out the carrier board for the compute module! Now we can actually get started with making it!

So now let's start a new KiCad project and get started!

Now the first thing I want to figure out is the connector because it's like the core part of the boards purpose.  Now there's MANY different options for board connectors, but personally I want something really rigid because I like to make my projects high quality. It also needs a LOT pins so pretty dense, so I have a couple of options I've compiled:
- **Board-to-board mezzanine connectors**: very compact, but lack a bit of rigidity, but they're also not crazy expensive and there's lots of variety in the connectors
- **SO-DIMM edge card connector**: pretty compact but larger, pretty darn rigid, more expensive, and sometimes messes with RF tests and stuff apparently?

Now personally I think I'm going to go with the SO-DIMM edge card connector because I have the space of an ITX motherboard which is pretty huge and it's also got really nice rigidity and looks very high quality. Another advantage of the SO-DIMM is that's it's compatible with the Turing RK1 which I kind of want to get my hands on and make compatible with this board.

![Pasted image 20250831115510.png](journal/Pasted%20image%2020250831115510.png)

Now before I actually add this to the schematic, I'm going to clone this CM4 carrier template which just provides the exact dimensions for a carrier board so I don't accidentally mess up the very fine measurements https://github.com/ShawnHymel/rpi-cm4-carrier-template. I found this from this very helpful resource page from [Maker Forge](https://www.makerforge.tech/posts/cm5-carrier-basics/), which gives really good tips for making a carrier board and they also have a journal of them [making an actual carrier board](https://www.makerforge.tech/cm5-carrier-board/) too.

And just like that, we have a nice template for our carrier board and there's also a schematic for the mezzanine connectors pre-made so it's easy to add stuff to it!

![Pasted image 20250831225318.png](journal/Pasted%20image%2020250831225318.png)

And for now I'm just going to end it there because we've actually started working on the project and got a lot of the specs for the carrier board down!

## Day 7 - Starting the PCB - 8 Hours

Now that I have the compute module template down, I can actually get started working on it! 

The first thing I'm going to do, is figure out what connector I'm going to use for the backplane. And before I mentioned I was going with SODIMM, but after some more research, it might not be the best fit.

I need a connector that can handle mid-high speed traces, around 60 - 70 pins and be decently, but not too compact. So the options I've compiled are:
- SO-DIMM: Very rigid and compact, can handle high speeds, 200+ pins, expensive
- MICRO-DIMM: Rigid and very compact, can handle high speeds, 50+ pins, hard to source and expensive
- 0.8mm 60+ pin vertical mezzanine connector: Compact, can handle mid speeds, 60+ pins, easy to source and relatively cheap

And it's honestly an insanely tough choice between SO-DIMM and the vertical mezzanine connector, because while the mezzanine connector is way cheaper, it's not as rigid and sleek as the SO-DIMM. Also another advantage of the SO-DIMM, is that it's compatible with the Turing RK1 and lots of other daughter boards, so I honestly think I'm going to go with SO-DIMM.

Now the Turing RK1 uses a 260 pin SO-DIMM connector, so that's the same thing I'm going to use for my board. 

Now I'm actually going to create custom symbols because I'm having trouble finding some online and they're relatively simple. I'm going to create 6 (a, b, c, d, e, f) symbols, each with 40 pins to make it manageable. I'm just going to take the 200 pin connector and add on some more to make it easy! And just like we're done!

![Pasted image 20250901173123.png](journal/Pasted%20image%2020250901173123.png)

Now the Turing RK1 doesn't actually have a listed pinout, but it's the same one as the [Jetson Orgin carrier board](https://developer.download.nvidia.com/assets/embedded/secure/jetson/orin_nano/docs/Jetson-Orin-Nano-DevKit-Carrier-Board-Specification_SP-11324-001_v1.3.pdf?__token__=exp=1756774659~hmac=b387e6facfb238adbd28ccc2a997d7d18f1f6ecd9e7dd8d21f77d45d6cec9db7&t=eyJscyI6ImdzZW8iLCJsc2QiOiJodHRwczovL3d3dy5nb29nbGUuY29tLyJ9) so I have to use that as reference! And I already know I'm in for a really complicated project....

So here's all the features I need:
- USB-C/USB 3.2
- Gigabit Ethernet
- Display Port
- M.2 Key E connector
- Expansion header
- UI and indicators
- Fan connector
- Power

I decided to include the M.2 Key E connector, because I figured out that it's only the M connector that's complicated to route and the E connector still gives me features like a network card and stuff I can add on.

This list was pretty much taken from the Jetson Orin carrier board datasheet, because it's the features I need to expose so that's it's supported!

So let's get started with putting the first thing down, the first thing I learned is that SODIMM is actually 2 sided, so 130 pins on one side, 130 on the other, so I redid my symbol to be a bit more accurate!

![Pasted image 20250901182004.png](journal/Pasted%20image%2020250901182004.png)

And then I actually realized that the A and the B have to be at the start of the number (to look good....) so I re-did it again because I'm a perfectionist. And then after that I labelled all the GND's on my schematic based off of the jetson orin carrier board pinout.

![Pasted image 20250901194745.png](journal/Pasted%20image%2020250901194745.png)

And turns out, I was looking at the wrong datasheet, the one I was looking at was for the carrier board of the nano, and not the nano itself (which already has SODIMM so it doesn't need a carrier for SODIMM). [So this is the right datasheet](https://developer.download.nvidia.com/assets/embedded/secure/jetson/orin_nx/docs/Jetson_Orin_NX_Orin_Nano_Pin_Function_Names_Guide_DA-11434-001_v1.0.pdf?__token__=exp=1756784920~hmac=4e1bb813f3562bd7b8484fd6d26ed09d41b7602d230afc62c7dfb80b68671c15&t=eyJscyI6ImdzZW8iLCJsc2QiOiJodHRwczovL3d3dy5nb29nbGUuY29tLyJ9).

So NOW, I actually have the right ground pins for my SODIMM:

![Pasted image 20250901204330.png](journal/Pasted%20image%2020250901204330.png)

And next, I'm going to add the power to my board. Now the CM5 takes a 5V input, so I'm going to handle the power management on the cluster board, and then just route it through the SODIMM into the mezzanine connector directly. But I do need some decoupling on the daughter card, but there's no datasheets to help me, because it's kind of the edge case of making a carrier board (you're not following like an IC datasheet, but making your own module), so I kind of have to figure out decoupling myself.

I decided to put one 0.1uF cap for every VDD pin (9), and then do a 10uF cap for each GROUP of VDD pins (2), and this gives me good high frequency and bulk decoupling for the power lines which I think is a good balance.

![Pasted image 20250902122459.png](journal/Pasted%20image%2020250902122459.png)
And I'm following the NVIDIA Jetson pinout for the SODIMM, so all the VDD pins are just near the end of the connector, and I think that pin 260 is just unused, and for mechanical usage, but I'm not 100% sure.

![Pasted image 20250902122555.png](journal/Pasted%20image%2020250902122555.png)
Now for most of the rest of these pins, I'm going to have to look at the [CM5 datasheet](https://datasheets.raspberrypi.com/cm5/cm5-datasheet.pdf) and wire to be pin compatible with the NVIDIA Jetson pinout which requires careful attention.

The first big thing I want to get out of the way, is wiring all the USB pins. It took me quite a long time, but you basically just have to wire the USB lines from the CM5, to the SODIMM while making sure you don't mess up the pinout of the NVIDIA Jetson so it requires careful attention.

The 2 standout things while wiring it was the USB_VBUS, which let's the BMC control the power on the USB ports so that's going to need a load switch on the cluster board, and then the NVIDIA Jetson has 3 USB 3.x ports while the CM5 only has 2, so I didn't wire the third. And just like that, it looks amazing!

![Pasted image 20250902145720.png](journal/Pasted%20image%2020250902145720.png)
![Pasted image 20250902145741.png](journal/Pasted%20image%2020250902145741.png)

Next up, I decided to wire up the ethernet onto my board. Ethernet has 4 differential pairs which all need to be wired to the SODIMM from the CM5 mezzanine connector, but it also has status LED's which need to be wired too. 

Now you can wire these status LED's onto the actual daughter card, or you can break them out onto the SODIMM. I decided to break out the 2 status LED's for activity and speed to the SODIMM, and then put the Pi activity LED onto the daughter card to show it's on.

It wasn't too complicated to figure out, but getting this concept though my head was a bit challenging. I decided to just breakout the LED's because that's what the NVIDIA Jetson does, and I kind of want to stay as pin compatible and concise as possible.

And just like that, we have ethernet wired up!

![Pasted image 20250902180206.png](journal/Pasted%20image%2020250902180206.png)
![Pasted image 20250902180225.png](journal/Pasted%20image%2020250902180225.png)

And then after this, I realized that some of my net labels were facing the wrong way (for input/output/bidirectional) and also, I was MISSING some USB lines too!!!! So I fixed those pretty quickly and it looks much better now!

![Pasted image 20250902181823.png](journal/Pasted%20image%2020250902181823.png)

Next, I want to implement the fans, I'm really just going in a kind of random order, but I want to tackle on the easier pins first. The fans just need PWM and Tacho (Not Taco!!!). Tacho is basically an output pin that the CM5 implements for fans that let you read it's current RPM, it's pretty cool and PWM just lets you control the fans.

It was a bit weird, because the pins on the CM5 symbol said they belong to ethernet, but they're actually multiplexed as both ethernet pins AND PWM/Tacho, and I didn't need the 2 ethernet pins I used, so I just made them fan pins.

And just like that, we're done implementing the fan pins!!!

![Pasted image 20250902201322.png](journal/Pasted%20image%2020250902201322.png)

Anyways I spent a pretty long time working on this, so I'm going to end it off here. This is some insanely good tangible progress though which always helps inspire me during my projects!

Tomorrow I'm going to try and get all the pins wired to the SODIMM, and then maybe start working on the eMMC or the NVMe wiring.

## Day 8 - SODIMM so cool! - 4 Hours

I made a lot of really good progress yesterday, so let's continue it!

The first thing I want to do is implement HDMI. HDMI isn't too complicated to wire, but routing is a different story... HDMI is pretty straightforward though, it's got 3 differential pairs of TX wires to drive to signals, and one differential pair of clock wires to keep everything synchronized.

And then, there's the I2C bus, SCL and SDA which are bidirectional and can transmit information like the display size and whatnot to the CM5. And to add on, there's also the HPD (hot plug detect) which just lets the source know if a device is plugged in, and there's the CEC (consumer electronics control), which just let's consumer signals be sent to the source like power on/off, audio, etc.

So it wasn't too complicated to wire, and just like that, we have HDMI implemented!

![Pasted image 20250903072920.png](journal/Pasted%20image%2020250903072920.png)
![Pasted image 20250903072940.png](journal/Pasted%20image%2020250903072940.png)

I also fixed a bunch of the net labels going the wrong way which I messed up for some reason, so you'll notice some changes there!

Anyways next, I wanted to implement SD cards onto the board, now there's 2 options of how I could do this:
- Put the SD cards on the cluster board and route them through the SODIMM connector
- Put the SD cards onto the daughter board and have them nicely self-contained

Now putting on the cluster board would add more routing and complexity, and the jetson also doesn't expose an SD card so it gets a bit confusing, so I think I'm going to include the SD card on the actual daughter card.

Now the only real problem with adding the SD card to the daughter card is space, but I honestly think it's going to be fine, and while it does make the daughter card slightly more expensive, I think it's worth it. So let's implement the SD card!

Now SD cards are pretty simple, I basically just route the signals from the mezzanine connector to the SD card directly, and just add decoupling to the power lines. Now the one thing you kind of want for something like this is a power switch so you can turn off the SD card if you're using eMMC or NVMe instead, so I need to add this little power switch circuit to the board.

I just took all of this from the CM5 datasheet, but I think it looks pretty good!

![Pasted image 20250904164726.png](journal/Pasted%20image%2020250904164726.png)

Some notes for this is that I'm wiring SD_PWR_ON, directly to the CM5, so the BMC doesn't actually control that, it's the CM5 that does. I did this because the NVIDIA jetson does the same thing, so it makes more sense to make everything the same.

And then after I did this wiring, I also added some labels just so the BMC can detect when the SD card is plugged in, just some fun added features and I also formatted it a bit more!

![Pasted image 20250904165741.png](journal/Pasted%20image%2020250904165741.png)

I'm honestly going to end the day off here, just because I don't have too much time because school just started, but I think I got some decent work done today!

## Day 9 - NVMe M.2 M-key slot! - 6 Hours

Now that I got SD cards implemented, I want to work on adding the M.2 M-Key slot which will allow us to plug in an SSD into the daughter board!

Now an M.2 M-Key slot is a connector that supports PCIe x4 lanes, used commonly for NVMe SSD's and has clock, reset and 4 differential lanes on it, so it's decently complicated to route/wire.

![Pasted image 20250905210937.png](journal/Pasted%20image%2020250905210937.png)

But the thing is, the CM5 only has x1 PCIe lanes exposed through the mezzanine connector, so with Gen 3 x1 PCIe so we only get around 1Gb/s of bandwidth. Now I want to go over how PCIe works a bit.

So PCIe has a bunch of different generations:

| Gen | Year | Data rate per lane   | Bandwidth x16 |
| --- | ---- | -------------------- | ------------- |
| 1.0 | 2003 | 2.5 GT/s (~250 MB/s) | ~4 GB/s       |
| 2.0 | 2007 | 5 GT/s (~500 MB/s)   | ~8 GB/s       |
| 3.0 | 2010 | 8 GT/s (~1 GB/s)     | ~16 GB/s      |
| 4.0 | 2017 | 16 GT/s (~2 GB/s)    | ~32 GB/s      |
| 5.0 | 2019 | 32 GT/s (~4 GB/s)    | ~64 GB/s      |
| 6.0 | 2022 | 64 GT/s (~8 GB/s)    | ~128 GB/s     |
Each generation gives more and more bandwidth, but not all are supported by the SoM. So the CM5 supports Gen 3.0, and exposed only one lane, so we get Gen 3.0 x1, which is 1Gb/s of bandwidth.

Now usually an SSD uses x4 lanes for high data transfer, but because we only have one lane exposed, we'll need to make do. 

The PCIe socket (where you plug the NVMe SSD into) also has some other pins like PEDET, which detects if a card is in it, and a bunch of other stuff, but we won't actually need those. But it's important to also wire the CLK/clock on the socket to keep accurate timing for the data flow, the clock is provided by the CM5.

Now I can choose to either wire the NVMe SSD onto the daughter card or put it on the cluster board by breaking it out through the SODIMM connector. It's actually a really tough choice, because putting it on the daughter card is much more simple, but the NVIDIA jetson and the turing rk1 break out the PCIe lanes through the SODIMM connector, so I wouldn't be able to give them an SSD.

So I think I'm actually going to breakout the M.2 M-Key lanes onto the cluster board so I'll also be able to support 4 lanes for the Turing RK1, and the NVIDIA jetson, but also support the one lane for the CM5/CM4.

But just to understand how the NVMe SSD wiring will work, I'm going to model it onto the daughter board and then actually wire it to the SODIMM, so I don't mess anything up!

Anyways, with a bit of research and some wiring, I think I have the wiring down!

![Pasted image 20250906121755.png](journal/Pasted%20image%2020250906121755.png)

And then on the SODIMM, I'll have just one lane, but for the Jetson and stuff, I'll wire all 4 lanes to the NVMe SSD on the actual cluster board for greater bandwidth!

Anyways, it's not too complicated to breakout the PCIe through the SODIMM connector because we're just using one lane with the CM5.

![Pasted image 20250906221641.png](journal/Pasted%20image%2020250906221641.png)

The next thing I'm going to do is, I'm going to breakout a camera onto the SODIMM connector. This is because the NVIDIA jetson has a BUNCH of camera's on it, and because I want to match the pinout, I want to include at least 1, and the CM5 has LOTS of camera lanes I can use (unlike the one lane of PCIe).

Now the NVIDIA jetson has 4, x2 camera's or 2, 4x lane camera's, so I'm just going to put one 4x camera and maybe use the other one for display port, or another camera if I can support it later, but for now, I know that I want the camera on it.

Camera's are pretty cool, they use the MIPI protocol, with differential pairs for data. Camera's like SSD's can run off x2 lanes, or x4 lanes, etc, for more bandwidth if you want and they also need I2C or SPI as a control interface. And then you'll probably want like a power reset pin to power the camera down or to reset it if it breaks.

The CM5 exposes 2, x4 MIPI CSI/DSI, so you can use them for either camera's or for the display serial interface (for some types of displays). I'm just going to wire one x4 lane for now, and then decide what to do with the last one later. The CM5 also exposes SDA/SCL pins for the camera's so I'll just use those, and then I'll use a GPIO for the PWDN.

There's also other pins you can provide to the camera protocol, like MCLK (master clock), which basically keeps timings on older/smaller camera's, but you honestly don't need those, and I don't think I'll be using those because I have longer traces for my camera's because they're on a different board.

Now let's implement camera's on my board! Most of the CSI lanes are on the high speed part of the mezzanine connector, so I can just grab those, and then use the I2C pins on the GPIO connector!

![Pasted image 20250908205540.png](journal/Pasted%20image%2020250908205540.png)
![Pasted image 20250908205626.png](journal/Pasted%20image%2020250908205626.png)

Now there's something a bit bizarre with the NVIDIA jetson, the pinout on my datasheet is 4, 2x lane camera's, but I want to do 2, 4x camera's because I don't have enough clock pins, so I have to hijack the data pins from another camera lane, and use them for the same lane.

![Pasted image 20250908205740.png](journal/Pasted%20image%2020250908205740.png)

*Only x2 lanes*

So by combining the pins/clocks, I get something like this:

![Pasted image 20250908205850.png](journal/Pasted%20image%2020250908205850.png)

Most of the camera lanes are near the start of the connector, and then the PWDN is a bit farther but I'm just following the pinout of the NVIDIA jetson so I won't question it.

And just like that, we've broken out a 4 lane camera interface!

I've implemented 2 of the more complicated protocols for today, so I think I'm going to end it off here. I'm definitely starting to slow down a bit more with the amount of work I've done and also school started too, but I'm going to try and grind this out now!

Tomorrow, I hope to implement lots of the debug headers and other things I need to interact with the actual board!

## Day 10 - Footprints and other shenanigans - 6 Hours

Today I want to just implement some of the other stuff I need on the daughter board like debug headers, RTC clock and whatnot.

The first thing I want to look at, is implementing an input for an RTC clock to make sure that the CM5 doesn't lose track of the time.

Now I was going to implement this, but I actually compared the CM4 and CM5 datasheet, and the pin is reserved on the CM4, but the CM5's pin is VBAT, so I don't actually want to implement it, because something will be connected to the reserved pin on the CM4 which isn't good.

Anyways, I'm getting a bit bored with breaking out pins on my SODIMM connector, so I'm going to start adding footprints into KiCad. The first footprint I want to add is the SODIMM **gold fingers** (I recently learned this term so don't mind if I didn't use it before, but it's basically the footprint for the SODIMM connector on the daughter board that plugs in). 

I've never used gold fingers before, but I learned that they're JUST a footprint, and not actually a connector like I thought before, and it's also a good idea to get ENIG if you're doing gold fingers, for board longevity.

It took a bit of scrolling, but I eventually found some KiCad footprints for the DDR4 gold fingers, and they look amazing!

![Pasted image 20250909191322.png](journal/Pasted%20image%2020250909191322.png)

Now I just have to add these onto my actual board. Because I used a "split" footprint for my SODIMM connector, I don't need to separate the footprint weirdly or group it, and instead I can just assign the gold fingers to the entirety of the footprint which is VERY convenient! So just like that we have the gold fingers in.

![Pasted image 20250909193119.png](journal/Pasted%20image%2020250909193119.png)

*That's a lot of connections...*

And then next, I want to add the SD card footprint onto my board, just so I can kind of visualize it a bit better! I want to use the same footprint on my 3DP motherboard because it's really small and SMD so you don't actually **need** to solder it on which is handy! (If you're curious, it's the microSD_HC_Hirose_DM3AT-SF-PEJM5 footprint).

![Pasted image 20250909193259.png](journal/Pasted%20image%2020250909193259.png)

Now I have the golden fingers in, but I don't actually have the correct size of the daughter board, so I'm going to steal from the SODIMM golden fingers footprint PCB, and just take their edge cut design. And after a bit of aligning, I got it down:

![Pasted image 20250909202738.png](journal/Pasted%20image%2020250909202738.png)

And then the next thing I did is I added the CM5/CM4 footprint onto the SODIMM connector, and then aligned everything to look really clean. The KiCad positioning tools and alignement were really useful for all of these!

![Pasted image 20250910181133.png](journal/Pasted%20image%2020250910181133.png)

After this, I wanted to put in the footprints for the capacitors I have so far. I'm going to try putting on the caps with 0603 footprints, just because it's easier to solder, but I might need to go smaller due to board space.

![Pasted image 20250916092310.png](journal/Pasted%20image%2020250916092310.png)

And from the size, they'll definitely need to be smaller, so I'm going to go with 0402 caps. Now I just realized that I probably don't need noise decoupling right by the golden fingers, and just on the mezzanine connector, so I'm going to just do one 0.1uF per pad on the VDD pin for the MEZZANINE connector, and then a bulk cap right by it too, and maybe a bulk cap by the golden fingers!

![Pasted image 20250916100555.png](journal/Pasted%20image%2020250916100555.png)

And then I realized that one cap per pin is a bit much, so I'm just going to do one per 2 pins. I'm also going to add a 1uF mid range cap just because I have the space to add one, and then I'm going to place all those alongside the SD card onto the board. The SD card is kind of in a temporary spot until I know exactly where to put it:

![Pasted image 20250916164945.png](journal/Pasted%20image%2020250916164945.png)

And then I added the rest of the passive I have so far and the status LED, this looks so cool!

![Pasted image 20250916171157.png](journal/Pasted%20image%2020250916171157.png)

Anyways, I got quite a bit done with the actual PCB today, so I'm going to end it off there. I'm a bit worried with my lack of passives, so I'm going to ask some questions about that. I'm also still missing some UART/SPI stuff, so I gotta figure that out too, and then breakout the rest of the GPIO's!

## Day 11 - Finessing spare GPIO's - 4 Hours

Now yesterday, I got the layout together, so now I want to focus on getting all the pin mappings done. The first thing I want to focus on is UART/SPI.

UART is really important for debugging your board and for communicating with peripherals like modems and such. It's pretty much essential if you want any hardware debugging and an extra protection in case your USB doesn't work or something so you can write to your board still.

SPI is really important for connecting external peripherals like sensors, display controllers, flash chips, etc. It's also good for high speed I/O, it's faster than I2C so it's useful for cluster boards, and you can have multiple peripherals on the same bus which is really cool. This basically means you can have 2 devices on the same SPI line, but choose which one talks at a time using the CS line, it's pretty cool!

The first thing I want to implement is SPI onto my board, it's fairly straightforward, the NVIDIA jetson exposes two hardware SPI controllers which 2 CS pins respectively so you can have multiple devices on each line.

![Pasted image 20250917192817.png](journal/Pasted%20image%2020250917192817.png)

The CM5 is cool, because the GPIO's can be toggled between UART/SPI/other protocols, so there's a lot of variety in what you can actually do:

![Pasted image 20250917193006.png](journal/Pasted%20image%2020250917193006.png)

So I'm just gonna use the SIO[0]/SIO[1] as the MOSI/MISO (which transmit data from master/slave essentially), and then just use 2 CS pins for each hardware controller.

So I carefully mapped these lines to the SODIMM connector following the NVIDIA Jetson pinout:

![Pasted image 20250917193149.png](journal/Pasted%20image%2020250917193149.png)
![Pasted image 20250917193205.png](journal/Pasted%20image%2020250917193205.png)

And just like that, we have SPI implemented. It was a bit complicated for me to understand how you can just use SIO as MOSI/MISO and the 2 CS pins, but I figured it out, and it should be working!

Next I need to implement UART! It's fairly simple, it has an RX/TX pair to just transmit data, and then there's optional RTS/CTS pins for hardware flow control. The SODIMM connector on the NVIDIA jetson exposes 2 hardware flow controllers for 2 of the UART controllers, and one without. These hardware flow controllers (CTS/RTS) let you basically know if data is ready to be transmitted or if it actually can be, so it's pretty helpful.

![Pasted image 20250918064933.png](journal/Pasted%20image%2020250918064933.png)

The CM5 multiplexes a bunch of the GPIO's like how I described earlier, but for UART, they also use GPIO0 and GPIO1, which are special, I need to use these because the other pins are being used by SPI.

![Pasted image 20250918065031.png](journal/Pasted%20image%2020250918065031.png)

Now GPIO0 and GPIO1 are special because they're also used for EEPROM for HAT's, but I'm pretty sure I don't need that, it just provides like information about the pi like vendor details and such, but I don't think I'll need to use those?

So instead I can use ID_SD and ID_SC as GPIO0 and GPIO1 for my UART controller, so I'm just going to map these from the CM5 mezzanine connector to the SODIMM breakout!

![Pasted image 20250918065555.png](journal/Pasted%20image%2020250918065555.png)
![Pasted image 20250918065614.png](journal/Pasted%20image%2020250918065614.png)

And just like that, we have 3 UART controllers, 2 of them with hardware flow control!

Next, I want to actually revisit the camera's. The NVIDIA jetson has support for 2 - 4 camera's, and I only have one implemented, so let's add the second one in. I didn't want to do this initially because I could also use it as a DSI interface, but I can just use HDMI for displays, so it's not really useful I feel like.

Anyways, just like the other camera controller, I'll just basically combine CSI2 and CSI3 on the NVIDIA jetson into one singular controller with double the lanes! This is because the CM5 has the lanes, but not the clock pins for more than 2 cameras:

![Pasted image 20250918185716.png](journal/Pasted%20image%2020250918185716.png)

I also cleaned up lots of the labels during this step, so the inputs/outputs, should be more accurate now!

![Pasted image 20250918185800.png](journal/Pasted%20image%2020250918185800.png)

Now that I have SPI, UART and the last camera in, I want to focus on using the rest of the GPIO's. The first thing I'm going to do, is see if I can create an I2C busses and wire those up for sensors and whatnot! My mezzanine connector is pretty full, but I just so happened to have GPIO22 and GPIO23 free for an I2C bus, so I'm going to add one there!

![Pasted image 20250918205413.png](journal/Pasted%20image%2020250918205413.png)
![Pasted image 20250918205452.png](journal/Pasted%20image%2020250918205452.png)

I2C is mostly used for just like sensors, peripheral control, like signals that can afford to be slow because it's a small 2 pin, bidirectional protocol. I might be able to also move around some pins to potentially get another I2C bus, but it's not the end of the world if I can't, but for now, at least I have one! 

Now I don't notice any more pins that I could possibly use for an I2C bus, so I'm just going to leave it for now.

I'm going to end it off there, because I really got done what I needed, and then tomorrow, I'll work on getting all the GPIO's in!

## Day 12 - GPIO's!! - 8 Hours

Now today is all about wiring all the GPIO's to give BMC functionality, do a bunch of information stuff, and for some other devices I'll bring out on the cluster board, there's just plenty to do with them.

I'm going to go pretty quick through all these because there's quite a few different ones, but I'll describe what each one is for.

The first thing I added what GPIO_CLK, which is a general purpose GPIO, but can also be a clock signal if needed! It's pretty darn cool!

![Pasted image 20250919174653.png](journal/Pasted%20image%2020250919174653.png)

Then I'm going to no-connect the MOD_SLEEP which just signals that the SoM is going into deep sleep, and the CM5 doesn't implement this.

MODULE_ID will also be no-connected because it's to tell the carrier what  jetson SKU is installed, which doesn't matter for the CM5!

FORCE_RECOVERY and SHUTDOWN_REQ will also not be connected because they're just shutdown stuff which the jetson handles, but the CM5 handles differently.

I'm going to be going through all the CM5 mezzanine pins after this to make sure that I didn't miss anything, so if any of these are wrong, I'll just re-wire!

After adding these no-connects, I wired up the SLEEP/RESET and the SYS_RESET pins. The CM5 doesn't have a SLEEP/RESET pin, so I just used a GPIO, I'm basically just using this to convey power states, but usually you'd use it to request a sleep/suspend instead of the POWER_EN which just shuts off power entirely.

Anyways I spent a long time not journalling in order to figure out a bunch of stuff. I realized that there's a lot of switching IO's, which aren't just GPIO's but like pins that are either GND or a certain voltage at some point. These use mosftets or transistors to switch, and they're required in order to follow jetson datasheets.

![Pasted image 20250924063355.png](journal/Pasted%20image%2020250924063355.png)

It's mostly all BMC pins, but basically the BMC will send a signal to these, and based off of the jetson datasheet, it will either be GND or a certain voltage that the MCU needs. There's also an LED that uses this type of mechanism to switch it on or off using an NPN.

![Pasted image 20250924063516.png](journal/Pasted%20image%2020250924063516.png)

Now NMOS's and NPN's are a bit different. NMOS is voltage based, so it switches based off of the voltage applied, whilst an NPN switches based off of the current and allows a larger current to flow from the collector to the emitter. It's kind of complicated but once you've used them a bit, they start to make sense.

I also added that 4 button switch on the board, so that you can manually tap the power button, reset, nRPI, and the PMIC EN.

Now I haven't talked about those 2 yet, but essentially, nRPI when held low, boots through USB 2.0 instead of eMMC, so it's just a recovery thing I implemented that probably won't be used too much, but it's good for a high quality board.

PMIC_EN will basically put the CM5 into low power state, which is just kind of nice to give the user and is relatively simple to wire.

And after an absurdly long time, and a bunch of other stuff I didn't talk about because it took so much focus, I got ALL the pins wired:

![Pasted image 20250924064040.png](journal/Pasted%20image%2020250924064040.png)![Pasted image 20250924064056.png](journal/Pasted%20image%2020250924064056.png)![Pasted image 20250924064112.png](journal/Pasted%20image%2020250924064112.png)

I also did a lot of small things, like add a pin 260 to go to power because I think one of the datasheets actually had a mistake in it and didn't include it, but another jetson datasheet had it.

I also removed some pins that weren't getting use like USB VBUS and such, and gave them real connections if they didn't have them yet.

Now I just need to level shift a BUNCH of signals to 1.8V, but I'll keep that for the next day.

Now it probably doesn't look like I did that much, but figuring out how to drive signals low, high, and whatnot took FOREVER, and was pretty darn complicated, so this day took over 8 hours to finish!

## Day 13 - Level shifting shenanigans - 13 Hours

Now today I need to figure out how to get a bunch of these signals from 3.3V to 1.8V. This is important so that I don't fry anything that the jetson would normally use at 1.8V by using it at 3.3V, and also so that things specifically looking for 1.8V don't mistake anything by seeing it at 3.3V, it's just generally pretty important.

Now the turing pi CM4 adapter, doesn't actually seem to include any level shifting on their board, and instead puts it on the cluster board, but I actually don't agree with this and I feel like it should be on the daughter board too. This is because if I want true pin compatibility, so that this card can be plugged in anywhere, other boards might not do the level shifting on the cluster board, so you could fry something or something might not be detected.

The level shifting is actually quite complicated to do in a nice manner though. I created this spreadsheet to explain to you guys, and to myself how this will work out:

![Pasted image 20251003202443.png](journal/Pasted%20image%2020251003202443.png)

So signals like camera power, reset and sleep don't need to be shifted on the board for various reasons.

Camera power doesn't need to be shifted because it's simple on/off. Module reset is a NMOS switch so I don't need that shifted too because it's just pulled up on the NMOS.

MOD_SLEEP is just detected when active low and the line is 3.3V tolerant, so it should be fine!

Anyways I actually forgot a bunch of information, so after many hours of research and testing, I came up with this combination:

![Pasted image 20251004214226.png](journal/Pasted%20image%2020251004214226.png)

The reason I don't use bidirectional transceivers is for lots of reasons like:
- Low drive current which causes parasitic capacitance which can cause mis-sampled bits
- Long lines, so you need efficient switching and driving current
- Slow switching speeds which isn't great for fast signals going in different directions like SPI

I think the unidirectional level shifters will be much more efficient.

Now this spreadsheet took me literally **13 hours** to come up with, it's probably one of the most complicated things I've had to wrap around my head to understand. I had to make an efficient IC setup with complicated signals, but it did take longer than it needed too, I was just really new to these concepts.

Anyways this is how I wired the whole thing:

![Pasted image 20251004214556.png](journal/Pasted%20image%2020251004214556.png)

A couple notes here:
- The decoupling capacitors are for the high-frequency switching transients, and then I added bulk caps because I'm working with really fast signals which can cause larger drops
- DIR is pulled down to specify that the direction is **B -> A**
- OE is pulled down to tell the transceiver to turn on

And after liker **13 hours**, I was finally done this absolute pain. I didn't mention my iteration because it was mostly user error, but this is just the facts on how I did it and why here!

## Day 14 - Design considerations - 12 Hours

Now we've actually finished up pretty much all the real wiring on our board, but now we just need to add the passives and protections.

Now we already have all of our decoupling in, but there's 2 things I feel like I have to add!

The first thing is termination resistors on lots of the high-speed lines. Termination resistors are basically resistors placed on a trace to match it's characteristic impedance, so it helps it keep it's proper impedance and manage signal integrity.

The second thing is ESD protection, this is important for high-speed data lines exposed to the user like ethernet, USB, etc. ESD protection helps prevent damage from static discharge that can occur. I haven't put too much effort into it, but I know that USB will probably need it, and maybe some other lines like ethernet!

Now before I even do this, I'm going to create a pinout table just so it's easier to plot my termination resistors and to make sure it matches up with the pinout of the jetson and whatnot. This took me about an hour and a half, but it's going to be pretty helpful:

![Pasted image 20251005124126.png](journal/Pasted%20image%2020251005124126.png)

*It's very long, and the full thing is accessible [here](https://docs.google.com/spreadsheets/d/1PQB4lJVr67ksKEhhsC4d91bklUIjZz4fbMR-MDZYI1U/edit?usp=sharing)*

Now before I even access my spreadsheet, I'm going to highlight the whole thing just to make sure everything is fine:

![Pasted image 20251006190738.png](journal/Pasted%20image%2020251006190738.png)

I didn't notice any possible issues, aside from a PCIe wake call (which I never added, but don't seem to need) and CM4/CM5 cross compatibility.

Now while I procrastinate checking out the CM4/CM5 compatibility, I want to start plotting the routing design for my high speeds signals. I'm going to be using what's called the Jetson Orin NX Nano Design Guide, which basically tells you the resistance, and extra components you'll want/should have on each controller to make sure that they can communicate properly:

![Pasted image 20251006204540.png](journal/Pasted%20image%2020251006204540.png)

So first let's talk about what USB2.0 needs, based off of this datasheet, we can see it has:
- Max frequency (isn't needed for routing considerations really)
- Max loading (you also don't really need to pay attention to this)
- Reference plane, this is important because it means that we need a GND plane close by basically so I need to remember to plan my stackup properly where the GND plane is closeby.
- Trace impedance, this is really important and very complicated so I'll explain it right after this
- Via proximity, this is kind of important but basically states how far away the reference plane needs to be from the via
- Max trace length is basically exactly what it says, it's how far your traces can go before wonky stuff starts happening. My traces are probably going to be pretty long so I need to research this a bunch
- Max intra-pair skew, this basically describes how accurate the impedance needs to be on the differential pairs, so basically length matching, it's pretty important.

Now let's talk about what the trace impedance is all about. Now there's 2 stat's here, SE (single ended impedance) and DP (differential pair impedance).

Single ended impedance is basically the impedance of a single trace relative to it's reference plane which is usually GND. This makes it so basically the signal can transmit properly by changing the physical geometry of the trace and signals around it, it's insanely interesting.

Differential pair impedance is basically the impedance between 2 traces calculated by taking the single-ended impedance and the coupling coefficient between the 2 traces (basically just how far apart they are), which also make the signals transmit properly.

So in my spreadsheet I'm going to keep track of the main points, pretty much all high speed signals follow the ground plane rule so I'm not going to mark it down, but the key points, I definitely will:

![Pasted image 20251007063144.png](journal/Pasted%20image%2020251007063144.png)

USB2.0:
- Max trace length: 6in
- Trace impedance: 90

Next we have USB3.0, this one's a lot more complicated because it's a way faster, so let's take a look at the design specs:
- Data rate: up to 10 GB/s which just tells us this is FAST 
- Max number of loads: this tells us that we shouldn't attach more than USB port to this controller
- Termination: this just tells us the differential we need to route our signals at
- Some electrical specifications we don't really need to care about unless they're dramatic, which they aren't really, just tells us we should probably add-on components
- Near end crosstalk basically tells us to avoid sharp bends on our traces and to not have too much noise around them
- Loss number tells us how much are signal is deteriorating every inch, this is going to be important for getting the max trace length
- The breakout region is the maximum gap between pairs when you're routing like BGA or something, this isn't actually relevant luckily because we're just routing them from a mezzanine connector which is pretty sweet!
- Intra-pair skew just tells us we need to length match well
- Uncoupled length limit tells us how far apart our differentials can comfortably be

and there's a bunch more, but those are directly relevant to the actual aspect of routing which we'll talk about soon:

![Pasted image 20251007064658.png](journal/Pasted%20image%2020251007064658.png)

So I noted down all the significant features of this design on the spreadsheet:

![Pasted image 20251007163846.png](journal/Pasted%20image%2020251007163846.png)

Next up we have PCIe 3.0. This is our highest speed signal so we need to pay the most attention to it. For Gen 4.0, which is 16 GB/s, you need to pay even more attention, but we're using 3.0 which is going to be more simple.

Now aside from all the other stuff, the datasheet specified that RX/TX should be 9x dielectric height spacing apart, which means they should be decently far apart, so definitely on different layers, which will help me plan my layer stackup!

Now I actually learned something here that I didn't realize USB3.0 also had. There's something called voiding, which is basically removing the GND/PWR fill underneath some pads/components to reduce parasitic capacitance and some other stuff, which is included in the datasheet.

So in USB3.0, it's suggested to void underneath the AC caps, and for PCIe 3.0, it's a good idea to void under the PCIe pads with 0.1mm+ tolerance!

Anyways after a bit of troubleshooting, I have solid design specs for PCIe gen 3.0:

![Pasted image 20251007171127.png](journal/Pasted%20image%2020251007171127.png)

Next up, we have ethernet! Ethernet is actually kind of boring and doesn't really need any add-on components like ESD, or AC caps, but it'll probably need some termination resistors, it's also not suggested to have via's, but it's fine for the PHY controller and whatnot:

![Pasted image 20251007173921.png](journal/Pasted%20image%2020251007173921.png)

![Pasted image 20251007174048.png](journal/Pasted%20image%2020251007174048.png)

Now let's design for HDMI. Now HDMI is special because it has a couple different ways of routing it:
- Stripline 2.1 - meets PCIe 2.1 standards, same layer (tightly coupled)
- Stripline 1.4b/2.0 - meets PCIe 1.4b/2.0 standards, same layer (tightly coupled)
- Microstrip 2.1 - meets PCIe 2.1 standards but routed on different layers (top/bottom)
- Microstrip 1.4b/2.0 - meets those standards and routed on different layers (top/bot)

Now I dived into this a bit, and it gets really interesting when you look at stuff like PCIe. Now you remember how PCIe TX/RX need to be routed on different layers, they're still stripline, because all the TX pairs are routed on the same layer, and all the RX ones on the same one too.

Stripline is more optimal than microstrip because the signals are more tightly coupled (lower crosstalk and better/easier impedance control).

Because of this, I'm going to go with a stripline design, which in term means we have specific trace requirements like 4x dielectric spacing and some different loss characteristics, nothing crazy important:

![Pasted image 20251007201106.png](journal/Pasted%20image%2020251007201106.png)

And then I just did the rest of them and updated this, I'm kind of just skipping the descriptions for these because it's really time consuming to describe:

![Pasted image 20251013134047.png](journal/Pasted%20image%2020251013134047.png)

SPI doesn't really need to be impedance matched, but I'm going to length match it because it's travelling really far!

Now I need to figure out how to do the dampening resistors! These are resistors to help reduce noise and to protect the board on signals that travel far and for a lot of other reasons. When I'm getting these fabricated, they're going to be 0 ohm resistors, and then you can desolder them and solder on values to test how it affects the noise.

They're very useful to optimize your board and important so your board works reliably and well. This actually took me really long to figure out, but eventually I figured out what signals should have them:
- USB DP/DM pairs should have them to reduce noise, but USB 3.0 shouldn't because those traces are much faster and it can mess with the impedance.
- HDMI TX should have them, and then I'll probably actually put some minor dampening resistors on the actual carrier board, but this is just to reduce ringing and to help match impedance
- CSI clock and transmit pairs should have them for noise again

This took me way too long to figure out, but it's pretty safe for dampening/impedance matching!

![Pasted image 20251013134336.png](journal/Pasted%20image%2020251013134336.png)
And then after that I made my schematic a bit easier to read, I'm not going to add all the screenshots, but all the schematics are now slightly easier to read!

Anyways, I did a lot, but it was a bit slow because everything needed really deep considerations. Next I need to layout all my components on my actual PCB, and add test points!

## Day 15 - Layout, test points, PCIe! - 12 Hours

Now that I've added all the dampening/termination resistors, I need to put them onto my board, fill all the footprints for my other components and group them together!

So first I need to add all my footprints in, this was really easy and the only hard part was looking at the datasheet for the level shifters and grabbing the footprint for it from there:

![Pasted image 20251013135121.png](journal/Pasted%20image%2020251013135121.png)

For my capacitors/resistors I follow the rule of, >10uF 0603+, <= 10uF, 0402-, and all resistors are just 0402. This gives good ESR characteristics on my capacitors and the resistors aren't too important from what I know. I don't really want to use under 0402 for this board, because I want it to be hand solderable, and also cheaper, potentially with economic PCBA!

And then I imported them and organized them all onto my board, this didn't take too long but gets me used to how everything will kind of fit on:

![Pasted image 20251013135427.png](journal/Pasted%20image%2020251013135427.png)

I really need to find a smaller button, and I'm pretty sure this is also a switch, but you get the idea!

Now I need to add in all the test points, which I've never done before, and have no idea how to do....

Anyways I found a new button, and then I used my intuition to figure out the test points, I just thought about what traces would probably be completely inaccessibly and weren't just simple GPIO's and I only needed one on my RTC battery to make sure that's working properly, and also one on my sleep mode status, which should automatically be sending:

![Pasted image 20251020064216.png](journal/Pasted%20image%2020251020064216.png)
And then, I also found this button, which has the same form factor as the one on the turing pi:

![Pasted image 20251020064304.png](journal/Pasted%20image%2020251020064304.png)

I then decided to flip my mezzanine connector so the high speeds were closer, which makes it a bit tighter to route, but I think it's better for ESR with smaller traces and lower loss.

Then, I did a ground pour on my 2 inner layers, so my stackup is now:

L1: PCIe RX
L2: GND
L3: Signal
L4: Signal
L5: GND
L6: PCIe TX

![Pasted image 20251020070417.png](journal/Pasted%20image%2020251020070417.png)

Now, I kind of want to find a way to fit a third ground plane in there, but I think the current stackup is acceptable.

Now before I start routing, I need to add what's called net classes to my labels. These are essentially like CSS classes, but for PCB's, you can give all the similar traces the same net class and they'll have the same sizes, constraints, etc. It's insanely cool.

Now when's I'll introduce the JLCPCB impedance calculator! This will basically tell me what size traces and stuff to do for routing specific things based off of your stackup:

![Pasted image 20251030065357.png](journal/Pasted%20image%2020251030065357.png)

And then I can just add these into my net classes for everything:

![Pasted image 20251030065452.png](journal/Pasted%20image%2020251030065452.png)

And then I can start routing everything:


![Pasted image 20251030064706.png](journal/Pasted%20image%2020251030064706.png)

These 3 steps took me a LONG time to figure out...

Also my routing in the last screenshot here is pretty terribly so I'll need to modify it to be more optimal. But before I do that, I'm going to do what's called voiding, which is removing GND underneath pads to reduce parasitic capacitance!

The golden fingers need 0.15mm of voiding around/under the pad, so I'll do something like this:

![Pasted image 20251030065727.png](journal/Pasted%20image%2020251030065727.png)


And then BOOM done!

## Day 16 - Routing HDMI, omg... 6 Hours

I got a LOT done on day 15, and now that I've finished PCIe, I want to work on HDMI, because it's close to that connector.

The one problem with routing HDMI is that there's also a lot of GPIO's I need to breakout and also I need to swap the polarity of HDMI midway through routing so that they can go into the connector. 

I'm going to just add a photo of how I did it and then describe it. This took 4 ITERATIONS, and wasn't too difficult, but extremely time consuming to make sure I wouldn't have too much crosstalk/skew!

![[Pasted image 20251102095312.png]]

Alright so let's breakdown what my thought process behind this routing was place down the dampening resistors in a way so that I had enough space to breakout the GPIO's and also so they were close enough to the differential pair.

My next thought was that these low speed signals won't exhibit much cross-talk so they can be closer to the high speed lines.

Now starting from the connector, you can see there's equal space between the top and bottom inside of the mezzanine connector. CSI is exhibiting cross-talk within 2x dielectric, so I made sure there was enough space there.

And then I followed the 3W rule for the middle differential pair because that one was running parallel to 2 other differential pairs which can exhibit strong electromagnetic forces so I wanted that one to be the farthest away.

