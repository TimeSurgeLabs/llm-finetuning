import openai
import sys

model = sys.argv[1]
filename = sys.argv[2]

file_obj = openai.files.create(
    purpose="fine-tune",
    file=open(filename, "rb")
)

job = openai.fine_tuning.jobs.create(
    training_file=file_obj.id,
    model=model
)
