# Keypirinha launcher (keypirinha.com)

import keypirinha as kp
import keypirinha_util as kpu
import keypirinha_net as kpnet

class Counter(kp.Plugin):
    """
    Counts the number of words, letters and occurences of an input
    """

    ITEMCAT_COUNTER = kp.ItemCategory.USER_BASE + 1
    ACTION_COPY_RESULT = "copy_result"

    def __init__(self):
        super().__init__()

    def on_start(self):
        self.set_actions(self.ITEMCAT_COUNTER, 
        [self.create_action(
            name=self.ACTION_COPY_RESULT,
            label="Copy Input",
            short_desc="Copy input to clipboard")])

    def on_catalog(self):
        catalog = []
        catalog.append(self.create_item(
            category=kp.ItemCategory.KEYWORD,
            label="Count",
            short_desc="Count the number of letters, words and occurences in an input.",
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
            words = user_input.lower().split()
            suggestions.append(self.create_item(
                    category=self.ITEMCAT_COUNTER,
                    label=f"{len(words)} Words / {len(user_input)} Characters",
                    short_desc=user_input,
                    target=user_input,
                    args_hint=kp.ItemArgsHint.FORBIDDEN,
                    hit_hint=kp.ItemHitHint.IGNORE))

            counts = {}
            for word in words:
                counts[word] = counts.get(word, 0) + 1

            pairs = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
            for word, count in pairs:
                suggestions.append(self.create_item(
                    category=self.ITEMCAT_COUNTER,
                    label=word,
                    short_desc=f"{word} ({count} Occurences)",
                    target=word,
                    args_hint=kp.ItemArgsHint.FORBIDDEN,
                    hit_hint=kp.ItemHitHint.IGNORE))
                
            self.set_suggestions(suggestions, kp.Match.ANY, kp.Sort.NONE)
        pass

    def on_execute(self, item, action):
        kpu.set_clipboard(item.target())
        pass