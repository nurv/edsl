import asyncio
import time

## TPM: Tokens-per-minute
## RPM: Requests-per-minute 

## TPM: 2,000,000
## RPM:    10,000

class TokenBucket:
    
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity  # Maximum number of tokens
        self.tokens = capacity  # Current number of available tokens
        self.refill_rate = refill_rate  # Rate at which tokens are refilled
        self.last_refill = time.monotonic()  # Last refill time

        self.log = []

    def __add__(self, other):
        return TokenBucket(capacity = min(self.capacity, other.capacity), 
                           refil_rate = min(self.refill_rate, other.refill_rate)
        )

    def refill(self):
        """Refill the bucket with new tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self.last_refill
        #print(f"Elapsed time: {elapsed}")
        refill_amount = elapsed * self.refill_rate
        #print(f"Refill amount: {refill_amount}")
        self.tokens = min(self.capacity, self.tokens + refill_amount)
        self.last_refill = now

        self.log.append((now, self.tokens))

    def wait_time(self, requested_tokens):
        """Calculate the time to wait for the requested number of tokens."""
        now = time.monotonic()
        elapsed = now - self.last_refill
        refill_amount = elapsed * self.refill_rate
        available_tokens = min(self.capacity, self.tokens + refill_amount)
        return max(0, requested_tokens - available_tokens) / self.refill_rate

    async def get_tokens(self, amount=1):
        """Wait for the specified number of tokens to become available."""
        if amount > self.capacity:
            raise ValueError(f"Requested tokens exceed bucket capacity. Bucket capacity: {self.capacity}, requested amount: {amount}")
        while self.tokens < amount:
            self.refill()
            await asyncio.sleep(0.1)  # Sleep briefly to prevent busy waiting
        self.tokens -= amount

        now = time.monotonic()
        self.log.append((now, self.tokens))

    def get_log(self):
        return self.log
    

    def visualize(self):
        from matplotlib import pyplot as plt
        times, tokens = zip(*self.get_log())
        start_time = times[0]
        times = [t - start_time for t in times]  # Normalize time to start from 0

        # Plotting
        plt.plot(times, tokens)
        plt.xlabel('Time (seconds)')
        plt.ylabel('Tokens Available')
        plt.title('Token Bucket Usage Over Time')
        plt.show()

# async def my_task(task_id, token_amount, bucket):
#     await bucket.get_tokens(token_amount)  # Request specified number of tokens from the bucket
#     print(f"Executing task {task_id} with {token_amount} tokens")
#     # Simulate task execution
#     await asyncio.sleep(1)

# async def main():
#     bucket = TokenBucket(capacity=10, refill_rate=2)  # Customize parameters as needed

#     # Example tasks with varying token requirements
#     tasks = [
#         my_task(1, 3, bucket),
#         my_task(2, 2, bucket),
#         my_task(3, 5, bucket),
#         my_task(4, 1, bucket)
#     ]
#     await asyncio.gather(*tasks)

# asyncio.run(main())
