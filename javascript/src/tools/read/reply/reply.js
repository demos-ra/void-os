export function reply(report, answer, relationalModel) {
    return relationalModel.dumps([...['file', 'not read', 'left behind', 'sheets'].flatMap((name) => report.filter((relation) => relation['sheet name'] === name)), ...answer]);
}
