import os
class Exporter:

    def __init__(self):

        pass

    def export_summary(

        self,

        validator,

        selector,

        cross_validator,

        optimizer

    ):

        os.makedirs(

            "outputs/reports",

            exist_ok=True

        )

        report = []

        report.append(

            "=" * 60

        )

        report.append(

            "ML INTELLIGENCE PLATFORM"

        )

        report.append(

            "=" * 60

        )

        report.append("")

        report.append(

            f"Dataset Quality : {validator.quality_score}/100"

        )

        report.append(

            f"Quality Label : {validator.quality_label}"

        )

        report.append("")

        report.append(

            "Model Comparison"

        )

        report.append(

            selector.results.to_string()

        )

        report.append("")

        report.append(

            "Cross Validation"

        )

        report.append(

            cross_validator.results.to_string()

        )

        report.append("")

        report.append(

            "Hyperparameter Optimization"

        )

        report.append(

            optimizer.results.to_string()

        )

        with open(

            "outputs/reports/summary_report.txt",

            "w",

            encoding="utf8"

        ) as file:

            file.write(

                "\n".join(report)

            )

        print()

        print("=" * 60)

        print("REPORT EXPORT")

        print("=" * 60)

        print()

        print("Summary report exported.")