export async function retryWithExponentialBackoff(fn, retries = 5, delay = 1000) {
    let attempt = 0;
    while (attempt < retries) {
        try {
            return await fn();
        } catch (error) {
            if (attempt === retries - 1) {
                throw error;
            }
            const backoffDelay = delay * Math.pow(2, attempt);
            console.warn(`Retrying in ${backoffDelay}ms...`);
            await new Promise(resolve => setTimeout(resolve, backoffDelay));
            attempt++;
        }
    }
}
