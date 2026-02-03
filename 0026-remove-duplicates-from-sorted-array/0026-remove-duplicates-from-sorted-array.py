class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        index = 0
        for s in range(len(nums)):
            if(nums[index] != nums[s]):
                index += 1
                nums[index] = nums[s]
                
        return index+1