export function kept(level, filter, relationalModel) {
    try {
        return relationalModel.kept(level, filter);
    }
    catch (error) {
        if (error instanceof relationalModel.RefusedError) {
            throw new RefusedError(error.message);
        }
        throw error;
    }
}
export class RefusedError extends Error {}
