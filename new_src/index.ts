import { Client, Interaction, Message, MessageActionRow, MessageButton, MessageEmbed, User } from "discord.js";
import QueueRepository from "./repositories/QueueRepository";

const NormClient = new Client({ intents: "GUILDS" });

// function called on startup
NormClient.on("ready", async () => {
  const channel = await NormClient.channels.fetch('629502331259584559')
  if (!channel) {
    throw new Error('Channel does not exist with id 629502331259584559');
  }
  if (!channel.isText()) {
    throw new Error('Channel is not a text channel!');
  }
  const row = new MessageActionRow()
    .addComponents(
      new MessageButton()
        .setCustomId('joinQueue')
        .setLabel('Join')
        .setStyle('SUCCESS')
        .setEmoji('✅'),
      new MessageButton()
        .setCustomId('leaveQueue')
        .setLabel('Leave')
        .setStyle('DANGER')
        .setEmoji('❌'),
      new MessageButton()
        .setCustomId('listQueue')
        .setLabel('List')
        .setStyle('PRIMARY')
        .setEmoji('\uD83C\uDDF1'), // Regional Indicator L
    );

  const embed = new MessageEmbed()
    .setColor('#3ba55c') // <- This is green
    .setTitle('Queue is Empty')
    .setDescription('Click the green button to join the queue!')
  console.info("NormJS is running.");

  await channel.send({ embeds: [embed], components: [row] });
});


NormClient.on('interactionCreate', async (buttonInteraction: Interaction) => {
  
  if (!buttonInteraction.isButton()) return;

  switch (buttonInteraction.customId) {
    case 'joinQueue': {

      //await QueueRepository.addBallChaserToQueue()

      const row = new MessageActionRow()
        .addComponents(
          new MessageButton()
            .setCustomId('joinQueue')
            .setLabel('Join')
            .setStyle('SUCCESS')
            .setEmoji('✅'),
          //.setDisabled(Need a method that returns T/F to determine if this is a clickable button after a full queue)
          new MessageButton()
            .setCustomId('leaveQueue')
            .setLabel('Leave')
            .setStyle('DANGER')
            .setEmoji('❌'),
          new MessageButton()
            .setCustomId('listQueue')
            .setLabel('List')
            .setStyle('PRIMARY')
            .setEmoji('\uD83C\uDDF1'), // Regional Indicator L
        );

      const embed = new MessageEmbed()
        .setColor('#3ba55c') // <- This is green
        .setTitle(buttonInteraction.user.username + ' Joined the Queue!')
        .setDescription('Click the green button to join the queue!\n\n' +
          await QueueRepository.getAllBallChasersInQueue() + ' h')

      await buttonInteraction.update({ embeds: [embed], components: [row] })
    }

    // Introduction of new error here after adding leave button. Join is called twice on the same interaction
    // Error [INTERACTION_ALREADY_REPLIED]: The reply to this interaction has already been sent or deferred.
    case 'leaveQueue': {

      //await QueueRepository.removeBallChaserFromQueue(buttonInteraction.user)

      const row = new MessageActionRow()
        .addComponents(
          new MessageButton()
            .setCustomId('joinQueue')
            .setLabel('Join')
            .setStyle('SUCCESS')
            .setEmoji('✅'),
          new MessageButton()
            .setCustomId('leaveQueue')
            .setLabel('Leave')
            .setStyle('DANGER')
            .setEmoji('❌'),
          new MessageButton()
            .setCustomId('listQueue')
            .setLabel('List')
            .setStyle('PRIMARY')
            .setEmoji('\uD83C\uDDF1'), // Regional Indicator L
        );

      const embed = new MessageEmbed()
        .setColor('#ed4245') // <- This is red
        .setTitle(buttonInteraction.user.username + ' Left the Queue!')
        .setDescription('Click the green button to join the queue!\n\n' +
          await QueueRepository.getAllBallChasersInQueue() + ' h')

      await buttonInteraction.update({ embeds: [embed], components: [row] })
    }

    case 'listQueue': {
      const row = new MessageActionRow()
        .addComponents(
          new MessageButton()
            .setCustomId('joinQueue')
            .setLabel('Join')
            .setStyle('SUCCESS')
            .setEmoji('✅'),
          //.setDisabled(Need a method that returns T/F to determine if this is a clickable button after a full queue)
          new MessageButton()
            .setCustomId('leaveQueue')
            .setLabel('Leave')
            .setStyle('DANGER')
            .setEmoji('❌'),
          new MessageButton()
            .setCustomId('listQueue')
            .setLabel('List')
            .setStyle('PRIMARY')
            .setEmoji('\uD83C\uDDF1'), // Regional Indicator L
        );

      const embed = new MessageEmbed()
        .setColor('#5865f2') // <- This is blurple
        .setTitle('List Of The Current Queue')
        .setDescription('Click the green button to join the queue!\n\n' +
          await QueueRepository.getAllBallChasersInQueue() + ' h\n\n h\n\n h')

      await buttonInteraction.update({ embeds: [embed], components: [row] })
    }
      break;

  }
})

NormClient.login(process.env.token);
