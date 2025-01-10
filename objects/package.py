class Package:
    def __init__(
        self,
        id: int | None,
        weight: float | None,
        gain: int | None,
        deadline: int | None,
    ) -> None:
        self.id = id
        self.weight = weight
        self.gain = gain
        self.deadline = deadline
        self.score = self.get_package_score()
        
    def get_package_score(self):
        """Tilldelar ett värde till ett paket"""
        dl_score =  - 15 ** (-1 * self.deadline)
        return dl_score - self.gain*20 + self.weight*4
    
