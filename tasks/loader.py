"""
Task 로더

_REGISTRY에 task ID → 모듈 경로를 등록하면 load_task()로 로드할 수 있다.
"""

import importlib

from tasks.base import Task

_REGISTRY: dict[str, str] = {
    "T-01": "tasks.T01_cooling_emergency",
    "T-02": "tasks.T02_vibration_escalation",
    "T-03": "tasks.T03_energy_overconsumption",
    "T-04": "tasks.T04_quality_hold",
    "T-05": "tasks.T05_multi_sla_breach",
    "T-06": "tasks.T06_emergency_shutdown_required",
    "T-07": "tasks.T07_shutdown_and_stabilize",
}


def load_task(task_id: str) -> Task:
    if task_id not in _REGISTRY:
        available = list(_REGISTRY.keys())
        raise ValueError(f"Task '{task_id}'를 찾을 수 없습니다. 등록된 task: {available}")
    module = importlib.import_module(_REGISTRY[task_id])
    return module.build()


def list_tasks() -> list[dict]:
    tasks = []
    for task_id, module_path in _REGISTRY.items():
        try:
            task = load_task(task_id)
            tasks.append({
                "id": task.id,
                "title": task.title,
                "policy_checks": len(task.policy_checks),
            })
        except Exception:
            tasks.append({"id": task_id, "error": "로드 실패"})
    return tasks
