# LMetr public-release checklist

Please complete these checks before creating a public tagged release or citing the repository as a fully reproducible software release.

- [ ] Confirm that all co-authors/rightsholders approve public source-code distribution.
- [ ] Choose and add an approved software license.
- [ ] Confirm the exact Ultralytics version in the original working environment and pin it in `requirements.txt`.
- [ ] Add the original optional GUI icon files to `icon/` if they are to be distributed.
- [ ] Test environment creation and application startup on a clean Windows machine.
- [ ] Test the full workflow using the Zenodo dataset and the exact YOLO weights used in the manuscript.
- [ ] Confirm the YOLO model weights can legally be redistributed or provide an accessible model-weight archive.
- [ ] Align the ExG implementation with the revised manuscript. The supplied source currently calculates `mean(2*G - R - B)` on raw channel values, not normalized chromatic coordinates.
- [ ] Confirm that the GLCM background handling described in the manuscript matches the implementation (masked-out pixels within the leaf bounding rectangle are set to zero and remain in the GLCM input).
- [ ] Add a software-version DOI after archiving a tagged GitHub release on Zenodo. The DOI currently included in README is the dataset DOI, not the software DOI.
- [ ] Check that the dataset DOI resolves to the intended public record and that the Zenodo record includes its dataset description and license.
