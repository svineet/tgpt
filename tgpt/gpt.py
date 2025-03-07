import openai

class GPTWrapper:
    def __init__(self, api_key, model="gpt-4o", system_prompt=None):
        self.api_key = api_key
        self.model = model
        self.SYSTEM_PROMPT = system_prompt

        self.conversation_log = (
            [{"role": "system", "content": self.SYSTEM_PROMPT}]
            if self.SYSTEM_PROMPT
            else []
        )

    def _send_request(self, prompt, use_log=False):
        if use_log:
            self.conversation_log.append({"role": "user", "content": prompt})

        response = openai.chat.completions.create(
            model=self.model,
            messages=self.conversation_log + [{"role": "user", "content": prompt}] if use_log else [{"role": "user", "content": prompt}],
        )

        if use_log:
            self.conversation_log.append(response.choices[0].message)

        return response.choices[0].message.content.strip()

    def add_post_execution_context(self, command, output):
        """
        Adds post-execution context to the conversation log.

        Parameters:
        - command (str): The command that was executed.
        - output (str): The output of the executed command.
        """
        self.conversation_log.append(
            {"role": "user",
             "content": f"<executor>\nCommand: {command}\nOutput:\n{output}"}
        )

    def send_with_log(self, prompt):
        response = self._send_request(prompt, use_log=True)
        return response

    def send_one_off(self, prompt):
        return self._send_request(prompt, use_log=False)
