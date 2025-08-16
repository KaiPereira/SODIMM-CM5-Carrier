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

I figured out that Bitluni basically had this carrier board, and then on that carrier board, it had these connectors called PCIe which allowed fast data transfer but also to basically plug in cards to your board like a PC.

This was such a cool concept, creating a cluster of computers that acted as a swarm, from basically many mini computers, I had to make one too.

You already know how I function though, I needed to go a bit bigger than Bitluni so I started researching about carrier boards, specifically CM4 carrier boards. Basically, rasp pi makes these things called "pi compute modules" (CMx) which can basically plug into these types of motherboards using PCIe or other connectors to turn their plain PCB, into a devboard of sorts with extra features on the carrier board.

Jeff Geerling is a really interesting guy I came across who loves messing around with carrier boards like this, I'd highly suggest checking out his stuff and learning how it all works https://www.jeffgeerling.com/

Anyways, I kind of know exactly what I want to make now, a carrier board with custom compute modules for maximum power, it takes a bit of time to wrap your head around this concept of PCB's on PCB's but it's really cool. I also kind of want to go overkill, I never like making stuff that the ordinary person would make, so something that sounds impressive, like 100's of gb's of ram, or 100's of gpu's, just the wow factor.

I was on a plane basically doing all this research, so it gave me a solid 6 hours of time on research what exactly a carrier board is and how everything works, but I've only just scratched the surface.

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
- And then the 4 node modules'

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
