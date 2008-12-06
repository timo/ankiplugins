# This plugin shows a replaces the "Suspend" menu entry in anki with a submenu,
# listing all suspended tags, so you can sort it.

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ankiqt import mw
from anki.utils import parseTags, addTags
    
def setTagCallable(tag):
    def callable():
        tagCurrentCard(tag)
    return callable

def createTagsMenu():
    mw.tagsMenu = QMenu("Suspend", mw)
    mw.tagsMenu.setIcon(QIcon(":icons/media-playback-pause.png"))
    mw.tagsMenu.setText = mw.tagsMenu.setTitle
    updateMenu()

def updateMenu():
    mw.tagsMenu.clear()
    for t in parseTags(mw.deck.suspended):
        mw.tagsMenu.addAction(t, setTagCallable(t))

def tagCurrentCard(tag):
    mw.deck.setUndoStart(_("Suspend"))
    mw.currentCard.fact.tags = addTags(tag, mw.currentCard.fact.tags)
    mw.currentCard.fact.setModified()
    for card in mw.currentCard.fact.cards:
        mw.deck.updatePriority(card)
    mw.deck.setModified()
    mw.lastScheduledTime = None
    mw.reset()
    mw.deck.setUndoEnd(_("Suspend"))

def replaceMenu():
    # create the new menu
    createTagsMenu()

    # insert it into the "current" menu
    mw.mainWin.menuCurrent.insertMenu(mw.mainWin.actionSuspendCard, mw.tagsMenu)
    mw.mainWin.menuCurrent.removeAction(mw.mainWin.actionSuspendCard)

    # the app should do the same things to the menu as it would to the old button
    mw.mainWin.actionSuspendCard = mw.tagsMenu

    mw.connect(mw.tagsMenu, SIGNAL("aboutToShow()"), updateMenu)

mw.addHook("init", replaceMenu)
