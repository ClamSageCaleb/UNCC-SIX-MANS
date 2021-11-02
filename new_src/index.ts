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
        );

      const embed = new MessageEmbed()
        .setColor('#3ba55c') // <- This is green
        .setTitle(buttonInteraction.user.username + ' Joined the Queue!')
        .setDescription('Click the green button to join the queue!\n\n' +
        await QueueRepository.getAllBallChasersInQueue() + ' h')

      //await QueueRepository.addBallChaserToQueue(buttonInteraction.user)
      await buttonInteraction.update({ embeds: [embed] })
    }

    case 'leaveQueue': {
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
        );

      const embed = new MessageEmbed()
        .setColor('#ed4245') // <- This is red
        .setTitle(buttonInteraction.user.username + ' Left the Queue!')
        .setDescription('Click the green button to join the queue!\n\n' +
        await QueueRepository.getAllBallChasersInQueue() + ' h')

      //await QueueRepository.removeBallChaserFromQueue(buttonInteraction.user)
      await buttonInteraction.update({ embeds: [embed] })
    }
    break;
    
  }
})

NormClient.login(process.env.token);
