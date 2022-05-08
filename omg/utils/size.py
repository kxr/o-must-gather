
def num2human(
    num,
    form="{n:.2f} {u}B",
    factor=1024,
    unit_list=["", "K", "M", "G", "T", "P", "E", "Z", "Y"]
):
    for unit in unit_list:
        if factor > num or unit == unit_list[-1]:
            return form.format(n=num, u=unit)
        num /= factor
