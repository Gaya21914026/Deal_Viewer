class DealTemplateAdapter:

    @staticmethod
    def build_projection(template):
        projection = {}

        for field in template["visibleFields"]:
            projection[field] = 1

        for section in template["sections"]:
            for field in section["fields"]:
                projection[field] = 1
        print("PROJECTION OK :", projection)

        return projection

    @staticmethod
    def get_nested_value(data, path):
        keys = path.split(".")
        for key in keys:
            if isinstance(data, dict) and key in data:
                data = data[key]
            else:
                return None
        return data

    @staticmethod
    def apply_template(deals, template):
        sections = template["sections"]
        labels = template.get("labels", {})
        visibleFields = template["visibleFields"]

        final_result = []

        for deal in deals:
            deal_output = []

            
            for section in sections:
                section_fields = {}
                for field in section["fields"]:
                    value = DealTemplateAdapter.get_nested_value(deal, field)
                    label = labels.get(field, field)
                    section_fields[label] = value

                deal_output.append({
                    "section": section["name"],
                    "fields": section_fields
                })

            
            label_values = {}
            for field in visibleFields:
                value = DealTemplateAdapter.get_nested_value(deal, field)
                if value is not None:
                    label_values[field] = value

            deal_output.append({"labels": label_values})
            final_result.append(deal_output)
        print("ADAPTER OK :", deal.get("reference"))

        return final_result
