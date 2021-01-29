# Keypirinha launcher (keypirinha.com)

import keypirinha as kp
import keypirinha_util as kpu
import keypirinha_net as kpnet

class Counter(kp.Plugin):
    """
    One-line description of your plugin.
    """

    ITEMCAT_COUNTER = kp.ItemCategory.USER_BASE + 1
    ACTION_COPY_RESULT = "copy_result"

    def __init__(self):
        super().__init__()

    def on_start(self):
        self.FOLDER_PATH = 'res://%s/'%(self.package_full_name())
        actions = [
            self.create_action(
                name=self.ACTION_COPY_RESULT,
                label="Copy Input",
                short_desc="Copy input to clipboard"
            )]
        self.set_actions(self.ITEMCAT_COUNTER, actions)

    def on_catalog(self):
        catalog = []
        catalog.append(self.create_item(
            category=kp.ItemCategory.KEYWORD,
            label="Count",
            short_desc="Count the number of letters and words in an input.",
            target='count',
            args_hint=kp.ItemArgsHint.REQUIRED,
            hit_hint=kp.ItemHitHint.NOARGS))

        self.set_catalog(catalog)
        pass

    def on_suggest(self, user_input, items_chain):
        if not items_chain or items_chain[-1].category() != kp.ItemCategory.KEYWORD:
            return

        if len(user_input) > 0:
            suggestions = []
            suggestions.append(self.create_item(
                    category=self.ITEMCAT_COUNTER,
                    label=user_input,
                    short_desc="{} Characters".format(len(user_input)),
                    target=user_input,
                    args_hint=kp.ItemArgsHint.FORBIDDEN,
                    hit_hint=kp.ItemHitHint.IGNORE))

            suggestions.append(self.create_item(
                    category=self.ITEMCAT_COUNTER,
                    label=user_input,
                    short_desc="{} Words".format(len(user_input.split())),
                    target="url",
                    args_hint=kp.ItemArgsHint.FORBIDDEN,
                    hit_hint=kp.ItemHitHint.IGNORE))
                
            self.set_suggestions(suggestions, kp.Match.ANY, kp.Sort.NONE)
        pass

    def on_execute(self, item, action):
        kpu.set_clipboard(item.target())
        pass