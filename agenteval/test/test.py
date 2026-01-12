# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from typing import Optional, Dict
from pydantic import BaseModel, Field


class Test(BaseModel, validate_assignment=True):
    """A test case.

    Attributes:
        name: Name of the test.
        steps: List of step to perform for the test.
        expected_results: List of expected results for the test.
        initial_prompt: The initial prompt.
        max_turns: Maximum number of turns allowed for the test.
        hook: The module path to an evaluation hook.
        bedrock_prompt_session_attributes: Prompt session attributes specific to this test.
        bedrock_session_attributes: Session attributes specific to this test.
    """

    # do not collect as a pytest
    __test__ = False

    name: str
    steps: list[str]
    expected_results: list[str]
    initial_prompt: Optional[str] = None
    max_turns: int
    hook: Optional[str] = None
    bedrock_prompt_session_attributes: Dict[str, str] = Field(default_factory=dict)
    bedrock_session_attributes: Dict[str, str] = Field(default_factory=dict)
