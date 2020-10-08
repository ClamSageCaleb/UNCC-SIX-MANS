import Queue
import TestHelper
from typing import List
from EmbedHelper import ErrorEmbed, AdminEmbed
from discord import Role, Embed


def fill(roles: List[Role]) -> Embed:
    if(Queue.isBotAdmin(roles)):
        TestHelper.fillQueue()
        return AdminEmbed(
            title="Queue Filled",
            desc="Queue has been filled with fake/real players"
        )

    return ErrorEmbed(
        title="Permission Denied",
        desc="You do not have permission to fill the queue."
    )


def fillCap(roles: List[Role]) -> Embed:
    if(Queue.isBotAdmin(roles)):
        TestHelper.fillWithCaptains()
        return AdminEmbed(
            title="Queue Filled w/ Captains",
            desc="Queue has been filled with fake/real players"
        )

    return ErrorEmbed(
        title="Permission Denied",
        desc="You do not have permission to fill the queue."
    )


def flipCap(roles: List[Role]) -> Embed:
    if(Queue.isBotAdmin(roles)):
        TestHelper.flipCaptains()
        return AdminEmbed(
            title="Captains Flipped",
            desc="Captains have been flipped."
        )

    return ErrorEmbed(
        title="Permission Denied",
        desc="You do not have permission to flip the captains."
    )


def flipReport(roles: List[Role]) -> Embed:
    if(Queue.isBotAdmin(roles)):
        TestHelper.swapReportedPlayer()
        return AdminEmbed(
            title="Reported Player Swapped",
            desc="The player who reported has been swapped out."
        )

    return ErrorEmbed(
        title="Permission Denied",
        desc="You do not have permission to flip the reporting player."
    )
