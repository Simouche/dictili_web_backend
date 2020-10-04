import os
from queue import Queue


nlp_queue = Queue()
inference_1_queue = Queue()


def prepare_workers():
    from document_generation.workers import TranscriptionWorker, NLPWorker, InferenceEngine1

    transcription_worker = TranscriptionWorker(daemon=True)
    transcription_worker.start()

    nlp_worker = NLPWorker(queue=nlp_queue, daemon=True)
    nlp_worker.start()

    inference_worker = InferenceEngine1(queue=inference_1_queue, daemon=True)
    inference_worker.start()


if os.environ.get('RUN_MAIN', None) == 'true':
    prepare_workers()
