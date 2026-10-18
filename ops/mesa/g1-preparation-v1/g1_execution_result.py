"""No-run terminal classification; never treats numerical fit as G1 admission."""


def classify_execution(*, exit_code, timed_out=False, oom_killed=False,
                       outputs_present=False, outputs_fresh=False,
                       provenance_complete=False, reached_target_age=False,
                       expected_termination=False):
    """Consume independently verified evidence, not truthy strings or defaults."""
    flags = (timed_out, oom_killed, outputs_present, outputs_fresh,
             provenance_complete, reached_target_age, expected_termination)
    if any(type(flag) is not bool for flag in flags):
        reason = "BLOCK_INVALID_EXECUTION_EVIDENCE"
    elif timed_out:
        reason = "BLOCK_TIMEOUT"
    elif oom_killed:
        reason = "BLOCK_OOM"
    elif type(exit_code) is not int or exit_code != 0:
        reason = "BLOCK_EXIT_STATUS"
    elif not outputs_present:
        reason = "BLOCK_MISSING_OUTPUTS"
    elif not outputs_fresh:
        reason = "BLOCK_STALE_OUTPUTS"
    elif not provenance_complete:
        reason = "BLOCK_PROVENANCE"
    elif not expected_termination:
        reason = "BLOCK_TERMINATION"
    elif not reached_target_age:
        reason = "BLOCK_TARGET_AGE"
    else:
        reason = "READY_FOR_EXTRACTION_ONLY"
    return {"schemaVersion": "g1-execution-result/1", "status": reason,
            "extractionAllowed": reason == "READY_FOR_EXTRACTION_ONLY",
            "admissionAllowed": False}
