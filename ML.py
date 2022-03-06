from Simulation import Simulation
import tensorflow.compat.v1 as tf
import numpy as np
tf.disable_v2_behavior()


n_inputs=6
n_hidden=4
n_outputs=3

learning_rate=0.01

env=Simulation()
#initializer=(n_outputs)
X = tf.placeholder(tf.float32,shape=[1,n_inputs])
hidden=tf.layers.dense(X,n_hidden,activation=tf.nn.elu,kernel_initializer='variance_scaling')
logits=tf.layers.dense(hidden,n_outputs)
outputs=tf.nn.sigmoid(logits)
p_move=tf.concat(axis=1,values=[outputs,1-outputs])
action=tf.multinomial(tf.log(p_move),num_samples=3)
cp=tf.map_fn(fn=lambda t: t if tf.equal(tf.reshape(t,[]),1) else tf.unstack(tf.constant([-1],dtype=tf.int64)), elems=tf.unstack(action),dtype=tf.int64)
action=tf.reshape(cp,[1,3])
y=tf.to_float(action)
cross_entropy=tf.nn.sigmoid_cross_entropy_with_logits(labels=y,logits=logits)
optimizer=tf.train.AdamOptimizer(learning_rate)
grads_and_vars=optimizer.compute_gradients(cross_entropy)
gradients=[grad for grad,variable in grads_and_vars]
vari=[variable for grad,variable in grads_and_vars]

gradient_placeholders=[]
grads_and_vars_feed=[]
for grad,variable in grads_and_vars:
    gradient_placeholder = tf.placeholder(tf.float32,shape=grad.get_shape())
    gradient_placeholders.append(gradient_placeholder)
    grads_and_vars_feed.append((gradient_placeholder,variable))
training_op=optimizer.apply_gradients(grads_and_vars_feed)

init=tf.global_variables_initializer()
saver=tf.train.Saver()

def discount_rewards(rewards,discount_rate):
    discount_rewards=np.empty(len(rewards))
    cumulative_rewards=0
    for step in reversed(range(len(rewards))):
        cumulative_rewards=rewards[step]+cumulative_rewards*discount_rate
        discount_rewards[step]=cumulative_rewards
    return discount_rewards

def discount_and_normalize_rewards(all_rewards,discount_rate):
    all_discounted_rewards=[discount_rewards(rewards,discount_rate) for rewards in all_rewards]
    flat_rewards=np.concatenate(all_discounted_rewards)
    reward_mean=flat_rewards.mean()
    reward_std=flat_rewards.std()
    return [(discounted_rewards-reward_mean)/reward_std for discounted_rewards in all_discounted_rewards]

n_iterations = 200
n_max_steps=1000
n_games_per_update=6
save_iterations=10
discount_rate=0.95

with tf.Session() as sess:
    init.run()
    # print(action.eval())
    for iteration in range(n_iterations):
        all_rewards=[]
        all_gradients=[]
        for game in range(n_games_per_update):
            current_rewards=[]
            current_gradients=[]
            obs=env.reset(game)
            if game==0:
                strv='Data/Gen/'+str(iteration)+'.txt'
                with open(strv, 'w') as file:
                    file.write("Keuwl Accelerometer Data File\n")
                    file.write("2021-11-24 09-07-13\n\n")   #file with data
                    file.write ("Time (s), X (m/s2), Y (m/s2), Z (m/s2), R (m/s2), Theta (deg), Phi (deg)\n")   #data format
                    for step in range(n_max_steps):
                        action_val,gradients_val = sess.run([action,gradients],feed_dict={X:obs.reshape(1,n_inputs)})
                        file.write(str(step)+",")
                        for i in action_val[0]:
                            file.write(str(i)+",")
                        file.write(str(0)+"\n")
                        obs,reward,done,info=env.step(action_val[0])
                        current_rewards.append(reward)
                        current_gradients.append(gradients_val)
                        if done:
                            break
            else:
                for step in range(n_max_steps):
                        action_val,gradients_val = sess.run([action,gradients],feed_dict={X:obs.reshape(1,n_inputs)})
                        obs,reward,done,info=env.step(action_val[0])
                        current_rewards.append(reward)
                        current_gradients.append(gradients_val)
                        if done:
                            break
                
            all_rewards.append(current_rewards)
            all_gradients.append(current_gradients)

        all_rewards =discount_and_normalize_rewards(all_rewards,discount_rate)
        feed_dict = {}
        for var_index, grad_placeholder in enumerate(gradient_placeholders):
            mean_gradients=np.mean([reward*all_gradients[game_index][step][var_index] for game_index,rewards in enumerate(all_rewards) for step, reward in enumerate(rewards)],axis=0)
            feed_dict[grad_placeholder]=mean_gradients
        sess.run(training_op,feed_dict=feed_dict)
        if iteration%save_iterations == 0:
            print ("save")
            saver.save(sess,"./moja_polityka_sieci_pg.ckpt")

print ("Finish")
