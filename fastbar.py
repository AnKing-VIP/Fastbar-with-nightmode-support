# -*- coding: utf-8 -*-
# pylint: skip-file
#
# Fastbar: an Anki 2.1 add-on adds a toolbar and toggle the sidebar
# in the Card Browser of Anki 2.1.
# Version: 0.1.1
# GitHub: https://github.com/luminousspice/anki-addons/
#
# Copyright: 2017 Luminous Spice <luminous.spice@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html
#
# Updated by The AnKing (https://www.ankingmed.com/)and /u/ijgnord
#
# Third party softwares used with Fastbar.
# QtAwesome. Copyright 2015 The Spyder development team.
# Released under the MIT License.
# https://github.com/spyder-ide/qtawesome/blob/master/LICENSE
# The Font Awesome is licensed under the SIL Open Font License.
# Six. Copyright 2010-2015 Benjamin Peterson
# Released under the MIT License.
# https://bitbucket.org/gutworth/six/src/LICENSE

# type: ignore

from aqt.qt import *
from PyQt5 import QtWidgets, QtCore
from aqt import mw
from aqt.forms.browser import Ui_Dialog
from aqt.browser import Browser
from anki.sched import Scheduler as schedv1
from anki.schedv2 import Scheduler as schedv2
from anki.utils import ids2str, intTime
from anki.hooks import addHook, wrap
from anki.lang import _

from . import qtawesome as qta


def gc(arg, fail=False):
    conf = mw.addonManager.getConfig(__name__)
    if conf:
        return conf.get(arg, fail)
    return fail


from anki import version as anki_version
old_anki = tuple(int(i) for i in anki_version.split(".")) < (2, 1, 20)
if old_anki:
    class Object():
        pass
    theme_manager = Object()
    theme_manager.night_mode = False
else:
    from aqt.theme import theme_manager


night_mode_on = False
def refresh_night_mode_state(nm_state):
    global night_mode_on
    if gc("switch to dark theme when add-on night mode is enabled"):
        night_mode_on = nm_state
addHook("night_mode_state_changed", refresh_night_mode_state)


class Fastbar:
    def addToolBar(self):
        tb = QToolBar("Fastbar")
        tb.setObjectName("Fastbar")
        if night_mode_on:
             tb.setIconSize(QtCore.QSize(90, 20))
        else:
            tb.setIconSize(QtCore.QSize(15, 15))
        tb.setToolButtonStyle(3)

        self.form.actionToggle_Sidebar.triggered.connect(lambda: self.sidebarDockWidget.toggleViewAction().trigger())
        self.form.actionToggle_Bury.triggered.connect(self.onBury)
        self.form.actionToggle_Fastbar.triggered.connect(lambda: tb.toggleViewAction().trigger())

        self.form.actionDelete.setText(_("Delete Note"))

        if night_mode_on or theme_manager.night_mode:
            icon_fastbar = qta.icon('ei.remove-sign', color="white")
            icon_sidebar = qta.icon('fa.exchange', color="white")
            icon_add = qta.icon('fa.plus-square', color="white")
            icon_info = qta.icon('fa.info-circle', color="white")
            icon_mark = qta.icon('fa.star', color="white")
            icon_suspend = qta.icon('fa.pause-circle', color="white")
            icon_bury = qta.icon('fa.step-backward', color="white")
            icon_deck = qta.icon('fa.inbox', color="white")
            icon_note = qta.icon('fa.leanpub', color="white")
            icon_tag = qta.icon('fa.tag', color="white")
            icon_untag = qta.icon('fa.eraser', color="white")
            icon_tag_unused = qta.icon('fa.magic', color="white")
            icon_delete = qta.icon('fa.trash-o', color="white")
            icon_resched = qta.icon('fa.history', color="white")
            icon_repos = qta.icon('fa.sign-in', color="white")
        else:
            icon_fastbar = qta.icon('ei.remove-sign')
            icon_sidebar = qta.icon('fa.exchange')
            icon_add = qta.icon('fa.plus-square')
            icon_info = qta.icon('fa.info-circle')
            icon_mark = qta.icon('fa.star')
            icon_suspend = qta.icon('fa.pause-circle')
            icon_bury = qta.icon('fa.step-backward')
            icon_deck = qta.icon('fa.inbox')
            icon_note = qta.icon('fa.leanpub')
            icon_tag = qta.icon('fa.tag')
            icon_untag = qta.icon('fa.eraser')
            icon_tag_unused = qta.icon('fa.magic')
            icon_delete = qta.icon('fa.trash-o')
            icon_resched = qta.icon('fa.sign-in')
            icon_repos = qta.icon('fa.history')
        
        if gc("enable compact mode"):
            # TODO: Create custom QToolBar widget to handle word-wrapping
            # properly
            for action_name in (
                "actionToggle_Fastbar", "actionToggle_Sidebar", "actionAdd",
                "action_Info", "actionToggle_Mark", "actionToggle_Suspend",
                "actionToggle_Bury", "actionChange_Deck", "actionChangeModel",
                "actionAdd_Tags", "actionRemove_Tags", "actionClear_Unused_Tags",
                "actionDelete", "actionReschedule", "actionReposition"
            ):
                action = getattr(self.form, action_name, None)
                if action is None:
                    continue
                action_text = action.text()
                if " " in action_text:
                    word_wrapped_text = action_text.replace(" ", "\n", 1)
                else:
                    # hacky way to align single-line labels
                    # "\n" contains an invisible space, since qt strips tailing whitespace
                    word_wrapped_text = action_text + "\n‎"
                action.setText(word_wrapped_text)

        self.form.actionToggle_Fastbar.setIcon(icon_fastbar)
        self.form.actionToggle_Sidebar.setIcon(icon_sidebar)
        self.form.actionAdd.setIcon(icon_add)
        self.form.action_Info.setIcon(icon_info)
        self.form.actionToggle_Mark.setIcon(icon_mark)
        self.form.actionToggle_Suspend.setIcon(icon_suspend)
        self.form.actionToggle_Bury.setIcon(icon_bury)
        self.form.actionChange_Deck.setIcon(icon_deck)
        self.form.actionChangeModel.setIcon(icon_note)
        self.form.actionAdd_Tags.setIcon(icon_tag)
        self.form.actionRemove_Tags.setIcon(icon_untag)
        self.form.actionClear_Unused_Tags.setIcon(icon_tag_unused)
        self.form.actionDelete.setIcon(icon_delete)
        self.form.actionReschedule.setIcon(icon_resched)
        self.form.actionReposition.setIcon(icon_repos)

        tb.addAction(self.form.actionToggle_Fastbar)
        #tb.addSeparator()
        tb.addAction(self.form.actionToggle_Sidebar)
        #tb.addSeparator()
        tb.addAction(self.form.actionAdd)
        #tb.addSeparator()
        tb.addAction(self.form.action_Info)
        #tb.addSeparator()
        tb.addAction(self.form.actionToggle_Mark)
        #tb.addSeparator()
        tb.addAction(self.form.actionToggle_Suspend)
        #tb.addSeparator()
        tb.addAction(self.form.actionToggle_Bury)
        #tb.addSeparator()
        tb.addAction(self.form.actionChange_Deck)
        #tb.addSeparator()
        tb.addAction(self.form.actionChangeModel)
        #tb.addSeparator()
        tb.addAction(self.form.actionAdd_Tags)
        #tb.addSeparator()
        tb.addAction(self.form.actionRemove_Tags)
        #tb.addSeparator()
        tb.addAction(self.form.actionClear_Unused_Tags)
        #tb.addSeparator()
        tb.addAction(self.form.actionDelete)
        #tb.addSeparator()
        tb.addAction(self.form.actionReschedule)
        tb.addAction(self.form.actionReposition)
        if night_mode_on:
            st = """
            QToolBar { background-color: #272828!important;
            background: #272828!important;
            spacing: 0px;
            color:  #272828!important;
            }
            QToolBar::separator{
                border: 0px solid #272828!important;
                background-color: #272828!important;
                background: #272828!important;
                margin-left: 0px;
                margin-right: 0px;
                width: 3px;
            }
            QToolButton {
                border: 0px solid #272828;
                border-radius: 0px;
                background-color: #272828;
                background: #272828!important;
                color:  #d7d7d7;
                margin-left: 0px;
                margin-right: 0px;
            }    
            QToolBar::handle {
                color: #272828;
                background:#272828;
                background-color: #272828;
            }
            QMacToolBar {
                border: 0px solid #272828!important;
                background-color: #272828!important;
                background: #272828!important;
                color: #272828!important;                
            }
            """
            tb.setStyleSheet(st)
        self.addToolBar(tb)

    def isBuried(self):
        if mw.col.schedVer() == 1:
            return not not (self.card and self.card.queue == -2)
        if mw.col.schedVer() == 2:
            return not not (self.card and self.card.queue in [-2, -3])

    def onBury(self):
        self.editor.saveNow(self._onBury)

    def _onBury(self):
        bur = not self.isBuried()
        c = self.selectedCards()
        if bur:
            self.col.sched.buryCards(c)
        else:
            self.col.sched.unburiedCards(c)
        self.model.reset()
        self.mw.requireReset()

    def unburiedCards(self, ids):
        "Unburied cards."
        self.col.log(ids)
        if mw.col.schedVer() == 1:
            self.col.db.execute(
                "update cards set queue=type,mod=?,usn=? "
                "where queue = -2 and id in "+ ids2str(ids),
                intTime(), self.col.usn())
        elif mw.col.schedVer() == 2:
            self.col.db.execute(
                "update cards set queue=type,mod=?,usn=? "
                "where queue in (-2,-3) and id in "+ ids2str(ids),
                intTime(), self.col.usn())
            

    def setupUi(self, Dialog):
        self.actionToggle_Sidebar = QtWidgets.QAction(Dialog)
        self.actionToggle_Sidebar.setObjectName("toggleSidebar")
        self.actionToggle_Sidebar.setText(_("Toggle Sidebar"))
        self.actionToggle_Bury = QtWidgets.QAction(Dialog)
        self.actionToggle_Bury.setText(_("Toggle Bury"))
        self.actionToggle_Bury.setText(_("Toggle Bury"))
        self.actionToggle_Fastbar = QtWidgets.QAction(Dialog)
        self.actionToggle_Fastbar.setObjectName("toggleFastbar")
        self.actionToggle_Fastbar.setText(_("Toggle Fastbar"))
        self.menuJump.addSeparator()
        self.menuJump.addAction(self.actionToggle_Sidebar)
        self.menuJump.addAction(self.actionToggle_Fastbar)
        self.menu_Cards.addSeparator()
        self.menu_Cards.addAction(self.actionToggle_Bury)

addHook("browser.setupMenus", Fastbar.addToolBar)
Browser.isBuried = Fastbar.isBuried
Browser.onBury = Fastbar.onBury
Browser._onBury = Fastbar._onBury
schedv1.unburiedCards = Fastbar.unburiedCards
schedv2.unburiedCards = Fastbar.unburiedCards

Ui_Dialog.setupUi = wrap(Ui_Dialog.setupUi, Fastbar.setupUi)
