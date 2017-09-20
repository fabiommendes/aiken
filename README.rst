.. These are the Travis-CI and Coveralls badges for your repository. Replace
   your *github_repository* and uncomment these lines by removing the leading
   two dots.

.. .. image:: https://travis-ci.org/*github_repository*.svg?branch=master
    :target: https://travis-ci.org/*github_repository*

.. .. image:: https://coveralls.io/repos/github/*github_repository*/badge.svg?branch=master
    :target: https://coveralls.io/github/*github_repository*?branch=master


This project is a Python parser for the Aiken question format used in Moodle. 
Aiken is a very simple format to represent multiple choice questions (https://docs.moodle.org/24/en/Aiken_format)
It accept two very similar syntaxes::

    What is the correct answer to this question?
    A. Is it this one?
    B. Maybe this answer?
    C. Possibly this one?
    D. Must be this one!
    ANSWER: D

And this::

    Which LMS has the most quiz import formats?
    A) Moodle
    B) ATutor
    C) Claroline
    D) Blackboard
    E) WebCT
    F) Ilias
    ANSWER: A 


Usage
=====

The aiken module simply expose the `load` and `dump` functions that respectively 
parse a question file and convert a parsed question object back to code. Let us
parse a question string:

>>> import aiken
>>> question = aiken.load("""
... Is this a valid Aiken Question?
... A. Yes
... B. No
... ANSWER: A
... """)
>>> question.options
['Yes', 'No']

Now, we make some changes and convert it back to a string of code:

>>> question.options.append('Who knows?')
>>> print(aiken.dump(question))
Is this a valid Aiken Question?
A. Yes
B. No
C. Who knows?
ANSWER: A
