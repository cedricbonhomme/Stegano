Contribution Guidelines
=======================

Before opening proposing any pull requests (about code or documentation),
please open an issue.

Code Contributions
------------------

When contributing code, you'll want to follow this checklist:

1. Fork the repository on GitHub.
2. Run the tests to confirm they all pass on your system. If they don't, you'll
   need to investigate why they fail.
3. Write tests that demonstrate your bug or feature. Ensure that they fail.
4. Make your change.
5. Run the entire test suite again, confirming that all tests pass *including
   the ones you just added*.
6. Send a GitHub Pull Request to the main repository's ``master`` branch.
   GitHub Pull Requests are the expected method of code collaboration on this
   project.

Code Style
~~~~~~~~~~

Please try to respect the `PEP 8`_ code style.


To get the greatest chance of helpful responses, please also observe the
following additional notes.

.. _PEP 8: http://pep8.org


Documentation Contributions
---------------------------

Documentation improvements are always welcome! The documentation files live in
the ``docs/`` directory of the codebase. They're written in
`reStructuredText`_, and use `Sphinx`_ to generate the full suite of
documentation.

When contributing documentation, please do your best to follow the style of the
documentation files. This means a soft-limit of 79 characters wide in your text
files and a semi-formal, yet friendly and approachable, prose style.

When presenting Python code, use single-quoted strings (``'hello'`` instead of
``"hello"``).

.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Sphinx: http://sphinx-doc.org/index.html



Good Bug Reports
----------------

Please be aware of the following things when filing bug reports:

1. Avoid raising duplicate issues. *Please* use the GitHub issue search feature
   to check whether your bug report or feature request has been mentioned in
   the past. Duplicate bug reports and feature requests are a huge maintenance
   burden on the limited resources of the project. If it is clear from your
   report that you would have struggled to find the original, that's ok, but
   if searching for a selection of words in your issue title would have found
   the duplicate then the issue will likely be closed extremely abruptly.
2. When filing bug reports about exceptions or tracebacks, please include the
   *complete* traceback. Partial tracebacks, or just the exception text, are
   not helpful. Issues that do not contain complete tracebacks may be closed
   without warning.
3. Make sure you provide a suitable amount of information to work with. This
   means you should provide:

   - Guidance on **how to reproduce the issue**. Ideally, this should be a
     *small* code sample that can be run immediately by the maintainers.
     Failing that, let us know what you're doing, how often it happens, what
     environment you're using, etc. Be thorough: it prevents us needing to ask
     further questions.
   - Tell us **what you expected to happen**. When we run your example code,
     what are we expecting to happen? What does "success" look like for your
     code?
   - Tell us **what actually happens**. It's not helpful for you to say "it
     doesn't work" or "it fails". Tell us *how* it fails: do you get an
     exception? A hang? A non-200 status code? How was the actual result
     different from your expected result?
   - Tell us **what version of Stegano you're using**, and
     **how you installed it**. Different versions of Stegano behave
     differently and have different bugs.

   If you do not provide all of these things, it will take us much longer to
   fix your problem. If we ask you to clarify these and you never respond, we
   will close your issue without fixing it.


Questions
=========

The GitHub issue tracker is for *bug reports* and *feature requests*. Please do
not use it to ask questions about how to use Stegano. These questions should
instead be directed to Stack Overflow. Make sure
that your question is tagged with the `python-stegano` tag when asking it on
Stack Overflow, to ensure that it is answered promptly and accurately.
You can search for questions with
`these tags <http://stackoverflow.com/questions/tagged/python+steganography>`_.
