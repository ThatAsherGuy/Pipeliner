# Pipeliner: The Airline for Italian Plumbers

Or, uh, something like that.

## The TL;DR

Pipeliner is a Blender add-on that aims to make consistent asset production easier. Need to tweak a setting in 30-some different .blend files? It'll help you do that. Need to export a bunch of FBX files using some weirdly specific configuration to keep your TD from skinning you alive? Pipeliner's your tool.

**NOTE:** This add-on hasn't hit 1.0 yet. There's a bunch of stuff here that *looks* like it should do things, but doesn't. Not yet. Also, I've done literally nothing to promote this add-on, so if you're reading this, it's likely because I've directly told you to as a part of whatever project you or I are working on.

## Feature Highlights

- A highly configurable set of batch export tools.
  - Export individual objects, whole collections, or intersections thereof, from multiple .blend files simultaneously.
  - Generate JSON manifests that model the semantic structure of multi-object assets, using collection colors to designate geometry types.
- Quick and easy object setup tools for creating UV channels and flood-filling vertex colors.
- Project-level productivity tools that make it easy to work with large groups of individual .blend files.

## Random Notes

- Blender can't recursively open file browsers; it's an inherent limitation that I can't hack my way around. This is why you have to separately specify the destination folder for the bulk exporter.
- At the moment, you'll have to call most of the operators via Operator Search. All of Pipeliner's operators are prefaced with 'Pipeliner:' in order to make this easier.
- The Churn List is a list of .blend files that's set with the 'Pipeliner: Set Churn List' operator. There's a whole set of 'Churn' operators that focus on navigating, and operating on, the Churn List.
- Operators that use Collection Colors refer to those colors by number rather than name. This is because Collection Color are configurable. And because I am colorblind.
- The Export Overrides for Objects are in the Item tab of the sidebar in the 3D viewport. The Export Overrides for Collections are in the Collection tab of the Properties Editor.
