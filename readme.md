# Github Repo Cleanup Tool

## About
I have a bunch of repositories, but I've let them get a bit
out of order. I needed a way to:

- Add a pre-determined set of milestones to all my projects
- Make "develop" the default branch
- Protect both the "develop" and "master" branches

I was able to find a [Python script that did the bit about migrating milestones](http://justinlee.sg/2013/07/16/importing-github-milestones-labels-issues-comments-from-one-repository-to-another/)
and then added my own work to change the default branch and protect the two
branches we wanted.

## References
- Justin Lee's blog post on [Importing Github Issues, Milestones, and Comments](http://justinlee.sg/2013/07/16/importing-github-milestones-labels-issues-comments-from-one-repository-to-another/)
- [Github v3 Repository API](https://developer.github.com/v3/repos/#enabling-and-disabling-branch-protection)

## License
Copyright 2016, Karl L. Hughes <khughes.me@gmail.com

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
