def compare(self, share_a: ABYShare, share_b: ABYShare, compare_type='lt', reveal_result=True, key="compare"):
        # share_diff = self.sub(share_a, share_b)
        shape_a = share_a.value.shape
        shape_b = share_b.value.shape
        if shape_a != shape_b:
            pygaialog.error("the shape of share_a and share_b is not equal, please check it first.")
            return 0
        share_a.value = share_a.value.flatten()
        share_b.value = share_b.value.flatten()
        tmp_min = 1 << (self.precision - 2)
        tmp_max = 1 << (self.precision - 1)
        value_random_1 = np.random.randint(tmp_min, tmp_max, share_a.value.shape)
        share_random_1 = ABYShare(value_random_1, share_a.scale)

        value_random_2 = np.random.randint(tmp_min, tmp_max, share_a.value.shape)
        share_random_2 = ABYShare(value_random_2, share_a.scale)

        share_random_a = self.mul(share_a, share_random_1, key=f"compare_mul_a{key}")

        share_random_a = self.add(share_random_a, share_random_2)
        share_random_b = self.mul(share_b, share_random_1, key=f"compare_mul_b{key}")
        share_random_b = self.add(share_random_b, share_random_2)
        value_random_a = self.reveal(share_random_a, key=f"reveal_random_a{key}")
        value_random_b = self.reveal(share_random_b, key=f"reveal_random_b{key}")
        value_random = value_random_a - value_random_b
        # print(f"vlaue_random = {value_random}")

        if compare_type == 'lt':
            value_random = np.array(np.array(value_random) < -0.000001, dtype=int)
        elif compare_type == 'gt':
            value_random = np.array(np.array(value_random) > 0.0000001, dtype=int)
        elif compare_type == 'gt_eq':
            value_random = np.array(np.array(value_random) > 0, dtype=int)
        elif compare_type == 'le':
            value_random = np.array(np.array(value_random) > 0.0000001, dtype=int)
            value_random = 1 - value_random
        elif compare_type == 'ge':
            value_random = np.array(np.array(value_random) < -0.0000001, dtype=int)
            value_random = 1 - value_random
        else:
            pygaialog.info("compare type cannot recognize, return less than result, the compare_type should be lt/gt ")
            value_random = np.array(np.array(value_random) < 0, dtype=int)

        value_random = value_random.reshape(shape_a)
        share_a.value = share_a.value.reshape(shape_a)
        share_b.value = share_b.value.reshape(shape_a)

        if not reveal_result:
            if self.role == 0:
                share_out = self.additive_share(value_random)
            else:
                share_out = self.get_share()

            return share_out

        return value_random
